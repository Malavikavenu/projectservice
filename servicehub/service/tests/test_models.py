from django.test import TestCase

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from django.db.utils import IntegrityError

from service.models import Customer,Work

from django.utils import timezone

class TestUserModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user=User.objects.create_user(
                                            username="testuser",
                                            email="testuser@mailinator.com",
                                            password="testpassword"
        )

    def test_create_user(self):

        user=User.objects.get(id=1)
        self.assertEqual(user.username,'testuser','username not same')
        self.assertEqual(user.email,'testuser@mailinator.com','mail not same')
        self.assertTrue(user.check_password('testpassword'))
    
    def test_string_representation(self):

        self.assertEqual(str(self.user),'testuser')

    def test_invalid_email(self):

        with self.assertRaises(ValidationError):
            user=User.objects.create_user(username="testuser12",email="invalid-email",password="testpassword")
            user.full_clean()

    def test_duplicate_username(self):

        with self.assertRaises(IntegrityError):

            user=User.objects.create_user(username="testuser",email="testuser123@gmail.com",password="testpassword")


class TestCustomerModel(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user=User.objects.create_user(username='testuser',password='testpassword')

        cls.customer=Customer.objects.create(
                                                name='testuser',
                                                phone='8394834543',
                                                email='testuser@mailinator.com',
                                                vehicle_number="kle1233",
                                                running_kilometer=3000,
                                                service_advisor=cls.user


                                            )

    def test_create_customer(self):

        customer_obj=Customer.objects.get(id=1)
        self.assertTrue(isinstance(customer_obj,Customer))
        self.assertEqual(customer_obj.name,'testuser')
        self.assertEqual(customer_obj.phone,'8394834543')
        self.assertEqual(customer_obj.email,'testuser@mailinator.com')
        self.assertEqual(customer_obj.vehicle_number,'kle1233')
        self.assertEqual(customer_obj.running_kilometer,3000)
        self.assertEqual(customer_obj.service_advisor,self.user)
        self.assertTrue(customer_obj.is_active)

    def test_string_representation(self):

        self.assertEqual(str(self.customer),'testuser')

    
    def test_created_date(self):

        self.assertIsNotNone(self.customer.created_date)
        self.assertLessEqual(self.customer.created_date,timezone.now())


    def test_updated_date(self):

        user=User.objects.create_user(username="testuser123",password="testpassword")
        customer=Customer.objects.create(name='testuser123',
                                        phone='8394834543',
                                        email='testuser@mailinator.com',
                                        vehicle_number='kle1233',
                                        running_kilometer=3000,
                                        service_advisor=user)

        
        customer.vehicle_number='kle8885'

        customer.save()

        self.assertIsNotNone(customer.updated_date)
        self.assertLessEqual(customer.updated_date,timezone.now())
        self.assertGreaterEqual(customer.updated_date,customer.created_date)


    def test_work_status(self):

        self.assertIsNotNone(self.customer.work_status)
        self.assertEqual(self.customer.work_status,'pending')
        self.assertIn(self.customer.work_status,dict(Customer.work_status_choices).keys())


    def test_invalid_work_status(self):
        with self.assertRaises(ValidationError):
            customer=Customer.objects.create(name='testuser123',
                                        phone='8394834543',
                                        email='testuser@mailinator.com',
                                        vehicle_number='kle1233',
                                        running_kilometer=3000,
                                        service_advisor=self.user,
                                        work_status='invalid status')
        
        
            customer.full_clean()


    def test_name_exceeds_max_length(self):
          customer=Customer.objects.create(name='testuser123'*200,
                                        phone='8394834543',
                                        email='testuser@mailinator.com',
                                        vehicle_number='kle1233',
                                        running_kilometer=3000,
                                        service_advisor=self.user)
          

          with self.assertRaises(ValidationError):
            customer.full_clean()

    
    def test_invalid_running_kilometer(self):
        with self.assertRaises(IntegrityError):
            
            Customer.objects.create(name='testuser123'*200,
                                        phone='8394834543',
                                        email='testuser@mailinator.com',
                                        vehicle_number='kle1233',
                                        running_kilometer=-3000,
                                        service_advisor=self.user)
        
    
    def test_invalid_phone_number(self):
        self.customer=Customer.objects.create(name='testuser123',
                                        phone='839',
                                        email='testuser@mailinator.com',
                                        vehicle_number='kle1233',
                                        running_kilometer=3000,
                                        service_advisor=self.user


                                        
                                        )
        
        with self.assertRaises(ValidationError):
            self.customer.full_clean()

         
        
          
class TestWorkModel(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user=User.objects.create_user(username='testuser',password='testpassword')

        cls.work=Work.objects.create(customer_object=cls.user,
                                     description='alloy changing',
                                     amoun=1000)
        

      

    def test_create_work(self):
        work_obj=Work.objects.get(id=1)

        self.assertTrue(isinstance(work_obj,Work))
        self.assertEqual(work_obj.customer_object,self.user)
        self.assertEqual(work_obj.description,'alloy changing')
        self.assertEqual(work_obj.amount,1000)
        self.assertTrue(work_obj.is_active)



        
        


    
















