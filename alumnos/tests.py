from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Alumno


class LoginFlowTests(TestCase):
    def setUp(self):
        self.alumno = Alumno.objects.create(
            dni="12345678",
            email="alumno@ipf.edu.ar",
            nombre_completo="Alumno Prueba",
            es_admin=False,
            is_active=True,
        )
        self.admin = Alumno.objects.create(
            dni="99999999",
            email="admin@ipf.edu.ar",
            nombre_completo="Admin Prueba",
            es_admin=True,
            is_active=True,
        )

    def test_login_page_loads(self):
        resp = self.client.get(reverse("alumnos:login"))
        self.assertEqual(resp.status_code, 200)

    def test_login_requires_terms(self):
        resp = self.client.post(reverse("alumnos:login"), {
            "dni": "12345678",
            "email": "alumno@ipf.edu.ar",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Debés aceptar los términos")

    def test_login_invalid_credentials_shows_error(self):
        resp = self.client.post(reverse("alumnos:login"), {
            "dni": "00000000",
            "email": "noexiste@ipf.edu.ar",
            "terms": "1",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "DNI o email incorrectos")

    def test_login_success_redirects_alumno(self):
        resp = self.client.post(reverse("alumnos:login"), {
            "dni": "12345678",
            "email": "alumno@ipf.edu.ar",
            "terms": "1",
        })
        self.assertRedirects(resp, reverse("alumnos:alumno_dashboard"), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username="12345678").exists())

    def test_login_admin_redirects_to_admin_dashboard(self):
        resp = self.client.post(reverse("alumnos:login"), {
            "dni": "99999999",
            "email": "admin@ipf.edu.ar",
            "terms": "1",
        })
        self.assertRedirects(resp, reverse("alumnos:admin_dashboard"), fetch_redirect_response=False)

    def test_inactive_alumno_cannot_login(self):
        self.alumno.is_active = False
        self.alumno.save()
        resp = self.client.post(reverse("alumnos:login"), {
            "dni": "12345678",
            "email": "alumno@ipf.edu.ar",
            "terms": "1",
        })
        self.assertContains(resp, "DNI o email incorrectos")

    def test_remember_me_sets_cookie_and_token(self):
        resp = self.client.post(reverse("alumnos:login"), {
            "dni": "12345678",
            "email": "alumno@ipf.edu.ar",
            "terms": "1",
            "remember_me": "1",
        })
        self.assertIn("alumno_remember", resp.cookies)
        self.alumno.refresh_from_db()
        self.assertIsNotNone(self.alumno.remember_token)

    def test_login_without_remember_does_not_set_cookie(self):
        resp = self.client.post(reverse("alumnos:login"), {
            "dni": "12345678",
            "email": "alumno@ipf.edu.ar",
            "terms": "1",
        })
        self.assertNotIn("alumno_remember", resp.cookies)


class LogoutTests(TestCase):
    def setUp(self):
        self.alumno = Alumno.objects.create(
            dni="12345678",
            email="alumno@ipf.edu.ar",
            nombre_completo="Alumno Prueba",
        )

    def test_logout_rejects_get(self):
        resp = self.client.get(reverse("alumnos:logout"))
        self.assertEqual(resp.status_code, 405)

    def test_logout_post_clears_remember_token(self):
        self.client.post(reverse("alumnos:login"), {
            "dni": "12345678",
            "email": "alumno@ipf.edu.ar",
            "terms": "1",
            "remember_me": "1",
        })
        self.alumno.refresh_from_db()
        self.assertIsNotNone(self.alumno.remember_token)

        resp = self.client.post(reverse("alumnos:logout"))
        self.assertRedirects(resp, reverse("alumnos:login"), fetch_redirect_response=False)
        self.alumno.refresh_from_db()
        self.assertIsNone(self.alumno.remember_token)


class AccessControlTests(TestCase):
    def setUp(self):
        self.alumno = Alumno.objects.create(
            dni="12345678",
            email="alumno@ipf.edu.ar",
            nombre_completo="Alumno Prueba",
        )

    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse("alumnos:alumno_dashboard"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("alumnos:login"), resp.url)

    def test_non_admin_cannot_access_admin_dashboard(self):
        self.client.post(reverse("alumnos:login"), {
            "dni": "12345678",
            "email": "alumno@ipf.edu.ar",
            "terms": "1",
        })
        resp = self.client.get(reverse("alumnos:admin_dashboard"))
        self.assertRedirects(resp, reverse("alumnos:alumno_dashboard"), fetch_redirect_response=False)
