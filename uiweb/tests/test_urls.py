from django.test import SimpleTestCase
from django.http import HttpRequest
from django.urls import reverse, resolve
from uiweb.views import home,login,storeRegistration,logout,profile,generateAdCoupon,generatePromoCode,passwordReset,activate_user

class Test_Urls(SimpleTestCase):

    def test_home_page_is_resolved(self):
        url= reverse('Home_Page')
        self.assertEquals(resolve(url).func,home)

    def test_login_page_is_resolved(self):
        url= reverse('Login')
        self.assertEquals(resolve(url).func,login)

    def test_store_registration_is_resolved(self):
        url= reverse('Store_Registration')
        self.assertEquals(resolve(url).func,storeRegistration)

    def test_logout_is_resolved(self):
        url= reverse('Logout')
        self.assertEquals(resolve(url).func,logout)    

    def test_logout_is_resolved(self):
        url= reverse('Logout')
        self.assertEquals(resolve(url).func,logout)    

    def test_profile_is_resolved(self):
        url= reverse('Profile')
        self.assertEquals(resolve(url).func,profile)    

    def test_GenerateAdCoupon_is_resolved(self):
        url= reverse('GenerateAdCoupon')
        self.assertEquals(resolve(url).func,generateAdCoupon)  

    def test_GeneratePromoCode_is_resolved(self):
        url= reverse('GeneratePromoCode')
        self.assertEquals(resolve(url).func,generatePromoCode)  

    def test_Password_Reset_is_resolved(self):
        url= reverse('Password_Reset')
        self.assertEquals(resolve(url).func,passwordReset)      



"""class HomePageTests(SimpleTestCase):
    
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('Home_Page'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('Home_Page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'uiweb/home3.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, 'Home_Page')"""        