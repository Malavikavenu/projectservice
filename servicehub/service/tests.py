from django.test import TestCase

class TestArithmatic(TestCase):

    def setUp(self):

        print("this is setup")

    @classmethod
    def setUpTestData(cls):
        
        cls.num1=20
        cls.num2=10

        print("this is setup test data")




    def test_addition(self):

        

        result= self.num1+self.num2
        self.assertEqual(result,30,"both are not same")


    def test_subtraction(self):

        

        result=self.num1-self.num2

        self.assertGreater(self.num1,0)#assert self.num1>0,"num1 should be > 0"

        self.assertEqual(result,10)

    def tearDown(self):
        print("testing finished")



      

    