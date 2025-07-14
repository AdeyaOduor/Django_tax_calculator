from django.test import TestCase, Client
from django.urls import reverse
import json

class TaxCalculatorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('calculate_tax')
    
    def test_valid_calculation(self):
        test_cases = [
            {'income': 200000, 'deductions': 20000, 'expected_tax': 18000},
            {'income': 300000, 'deductions': 30000, 'expected_tax': 27000 + 2250},
            {'income': 500000, 'deductions': 50000, 'expected_tax': 28800 + 25000 + 18600},
        ]
        
        for case in test_cases:
            response = self.client.post(
                self.url,
                data=json.dumps({
                    'income': case['income'],
                    'deductions': case['deductions'],
                    'year': '2023'
                }),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])
            self.assertAlmostEqual(data['results']['income_tax'], case['expected_tax'], places=2)
    
    def test_invalid_inputs(self):
        # Test negative income
        response = self.client.post(
            self.url,
            data=json.dumps({'income': -1000}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test missing income
        response = self.client.post(
            self.url,
            data=json.dumps({'deductions': 1000}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_rate_limiting(self):
        for _ in range(5):  # First 5 requests should work
            response = self.client.post(
                self.url,
                data=json.dumps({'income': 100000}),
                content_type='application/json'
            )
            self.assertIn(response.status_code, [200, 400])
        
        # 6th request should be blocked
        response = self.client.post(
            self.url,
            data=json.dumps({'income': 100000}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 429)