import pandas as pd

class Mortgage:
    def __init__(self, rate, loan, term, interest_only = False, points=0.0, other_fees=0.0):
        """
        Mortgage has the following attributes:
            1. rate. Rate is the interest rate per term unit.
            2. loan. Loan is the total loan amount for the mortgage
            3. term. The length of the loan.
            4. interest_only. A boolean for whether or not the loan is interest
            only. Defaults to False.
            5. points. The origination points for the loan on the basis of the
            term
            6. other_fees. A fixed number for the total miscelaneous fees for
            the loan.
        """
        # test for non empty, term is int, interest_only is bool
        self.rate = float(rate)
        self.loan = float(loan)

        if type(term) != type(int(1)):
            raise ValueError("Term must be an integer")

        self.term = term
        self.interest_only = interest_only
        self.points = float(points)
        self.points_amount = self.points * self.loan
        self.other_fees = float(other_fees)

    def get_pmt(self):
        """
        Will get pmt based on the time unit in __init__. You will determine to
        input monthly or annual rate and term
        """
        if self.interest_only:
            pmt = self.loan*self.rate
        else:
            pmt = self.loan*(self.rate + (self.rate/(pow(1+self.rate,self.term)-1)))
        return pmt

    def total_pmts(self, period):
        """
        Returns total mortgage payments up to and including period
        """
        return self.get_pmt() * period

    def get_amortization_table(self, format='pandas_df', decimal_places=2):
        """
        Format is either one of 'pandas_df' or 'json' to return either a Pandas
        DataFrame or a JSONized object from Pandas DataFrame
        """
        columns = ['PMT', 'BOP RMB','PPMT', 'IPMT', 'EOP RMB']
        df = pd.DataFrame(columns = columns, index = range(1,self.term+1))
        pmt = self.get_pmt()

        for i in range(self.term):
            df['PMT'][i+1] = pmt
            df['PPMT'][i+1] = self.get_principal_pmt(i+1)
            df['IPMT'][i+1] = pmt-df['PPMT'][i+1]
            if i==0:
                df['BOP RMB'][i+1] = self.loan
            else:
                df['BOP RMB'][i+1] = df['EOP RMB'][i]
            df['EOP RMB'][i+1] = df['BOP RMB'][i+1] - df['PPMT'][i+1]
        for c in columns:
            df[c] = df[c].map(lambda x: round(x, decimal_places))

        if format == 'json':
            return df.to_json()

        return df

    def get_apr(self):
        total_fees = self.points * self.loan + self.fees
        return None

    def get_interest_pmt(self, period):
        """
        Returns interest paid in one period
        """
        if self.interest_only:
            return self.get_pmt()
        else:
            cumulative_interest_pmt1 = self.cumulative_interest_pmt(period)
            cumulative_interest_pmt0 = self.cumulative_interest_pmt(period-1)
            return cumulative_interest_pmt1 - cumulative_interest_pmt0

    def get_principal_pmt(self, period):
        """
        Returns principal paid in one period
        """
        return self.get_pmt() - self.get_interest_pmt(period)

    def cumulative_interest_pmt(self, period):
        """
        Returns total interest paid in from first period up to and including
        period.
        """
        if self.interest_only:
            return self.total_pmts(period)
        total_pmts = self.total_pmts(period)
        total_principal_pmt = self.cumulative_principal_pmt(period)
        return total_pmts - total_principal_pmt

    def cumulative_principal_pmt(self, period):
        return self.loan - self.remaining_mortgage_balance(period)

    def remaining_mortgage_balance(self, ending_period):
        """
        Returns the remaining loan amount at ending_period
        """
        if ending_period==0:
            return self.loan
        else:
            return self.remaining_mortgage_balance(ending_period-1)*(1+self.rate) - self.get_pmt()

    def describe(self):
        """
        Print out information about the MOrtgage instance
        """
        print("\n===Describe Mortgage===\n")
        print("Interest Rate: \t", "{}%".format(round(self.rate*100,2)))
        print("Loan Amount: \t", "${}".format(round(self.loan,2)))
        print("Term: \t\t", self.term)
        print("Interest Only: \t", self.interest_only)
        print("Points: \t", self.points)
        print("Other Fees: \t", self.other_fees)
        print("Payment: \t", "${}".format(round(self.get_pmt(), 2)))
