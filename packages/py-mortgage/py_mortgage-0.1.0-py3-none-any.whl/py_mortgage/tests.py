import unittest
from mortgage import Mortgage

new_mortgage = Mortgage(rate = .04/12, loan = 400000, term = 360, interest_only=False)

# print("PMT:\t\t", new_mortgage.get_pmt())
# print("All PMTs:\t", new_mortgage.total_pmts(12), new_mortgage.total_pmts(12)==new_mortgage.get_pmt()*12)
# print("Interest PMTS:\t", new_mortgage.get_interest_pmt(12))
# print("Principal PMTS: \t", new_mortgage.get_principal_pmt(12))
# print(new_mortgage.get_amortization_table())
new_mortgage.describe()
class MyFirstTests(unittest.TestCase):
    def test_pmt(self):
        self.assertEqual(new_mortgage.total_pmts(12), new_mortgage.get_pmt()*12)

if __name__ == '__main__':
    unittest.main()
