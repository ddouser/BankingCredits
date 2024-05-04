import random
import math
from icecream import ic


class Macrosphere:
    gameActive = None
    tax_rate = None
    curr_credit_id = None
    global_interest_rate = None
    consumer_capacity_rate = None
    inflation = None
    current_year = None
    global_unemployment_rate = None
    budget = None
    bank_List = None
    company_List = None
    economic_cycles_s = ["Expansion", "Peak", "Contraction", "Trough"]
    economic_cycle_n = 1  # Фаза экономического цикла


    @staticmethod
    def initialise():
        Macrosphere.tax_rate = 0.2 # Tax Rate
        Macrosphere.global_unemployment_rate = 0.2  # Уровень безработицы
        Macrosphere.inflation = 1  # Уровень инфляции
        Macrosphere.current_year = 0
        Macrosphere.curr_credit_id = 0
        Macrosphere.bank_List = []
        Macrosphere.company_List = []
        Macrosphere.global_interest_rate = 5
        Macrosphere.consumer_capacity_rate = 0.5
        Macrosphere.budget = 10 * (1000 ** 2)

        for i in range(100):
            Macrosphere.company_List.append(company())
        bank1 = Bank(1000000)
        bank2 = Bank(1000000)
        ic(Macrosphere.bank_List)
        ic(Macrosphere.company_List)
        Macrosphere.gameActive = True
    @staticmethod
    def summarise():
        for company in Macrosphere.company_List:
            pass
        for bank in Macrosphere.bank_List:
            
            pass
        Macrosphere.payoff = Macrosphere.budget
    @staticmethod
    def countCredits():
        s = 0
        for i in Macrosphere.bank_List:
            for company in i.company:
                s += len(company.credits)

    @staticmethod
    def display_macro_factors():
        print(f"Year: {Macrosphere.current_year}")
        print(f"Unemployment Rate: {Macrosphere.global_unemployment_rate * 100}%")
        print(f"Economic Cycle: {Macrosphere.economic_cycles_s[Macrosphere.economic_cycle_n]}")
        print(f"Inflation Rate: {Macrosphere.inflation}%")
        print(f"Consumer_capacity_rate: {Macrosphere.consumer_capacity_rate}")

        for i in Macrosphere.bank_List:
            ic(i.debt)
        sum_debt = 0
        s0 = 0
        for i in Macrosphere.company_List:
            sum_debt += i.debt()
            for credit in i.credits:
                if credit.bank_id == 0:
                    s0 += credit.body
        print(f"Borrower sum_debt: {sum_debt}")
        print(f"Borrower sum_debt0  sum_debt1: {s0,sum_debt-s0}")

    @staticmethod
    def generate_credits(sum_credit, bank):
        if Macrosphere.budget >= 0:
            bank.balance += sum_credit
            bank.debt += sum_credit
            Macrosphere.budget -= sum_credit
        else:
            input("Macrosphere lost budget.")
        # Raise Interest? Tax?

    @staticmethod
    def calculus_end_day():
        for b in Macrosphere.bank_List:
            b.debt = round(b.debt * (1 + (Macrosphere.global_interest_rate) / 100) / (
                    1 + Macrosphere.inflation / 100))
            # Ask for credit?
        s = []
        for c in Macrosphere.company_List:
            s.append(c.employment_rate)
        old_c = Macrosphere.consumer_capacity_rate
        ic(s)
        Macrosphere.global_unemployment_rate = sum(s) / len(s)
        Macrosphere.consumer_capacity_rate = max(0, min(1, 0.6 * sum(s) / len(s) - 0.4 * (
                Macrosphere.inflation - Macrosphere.global_interest_rate) / Macrosphere.global_interest_rate))
        Macrosphere.inflation = max(0,
                                    min(100, Macrosphere.inflation + 0.3 * Macrosphere.consumer_capacity_rate - old_c))






class Credit:
    def __init__(self, body, interest_rate, credit_id, bank_id, company_id, result,period = 10):
        self.body = body
        self.initial_body = body
        self.interest_rate = interest_rate
        self.credit_id = credit_id
        self.bank_id = bank_id
        self.company_id = company_id
        self.date_given = Macrosphere.current_year
        self.result = result
        self.date_paid = Macrosphere.current_year+period


class Bank:
    def __init__(self, capital):
        self.capital = capital
        self.debt = 0
        self.company = []
        self.id = len(Macrosphere.bank_List)
        Macrosphere.bank_List.append(self)

    def determine_interest_rate(self, company):
        # Простая логика определения процентной ставки на основе рейтинга кредитора
        if self.id == 1 and Macrosphere.gametype == "1":
            return 5  # TODO GAME 1

        if company.rating > 750:
            return 5  # Низкий риск, низкая ставка
        elif company.rating > 500:
            return 10  # Средний риск, средняя ставка
        else:
            return 15  # Высокий риск, высокая ставка

    def score_company(self, company):
        company.rating = self.creditScore(company)
        Macrosphere.curr_credit_id += 1
        creditOffer = Credit(company.size, self.determine_interest_rate(company), Macrosphere.curr_credit_id,
                             bank_id=self.id, company_id=company.id, result=True)
        return creditOffer

    def creditScore(self, company):
        # Веса для каждого фактора
        w1, w2, w3, w4 = 0.25, 0.25, 0.25, 0.25

        age_effect_value = 1 - math.exp(-company.age / 5)
        profitability_effect_value = company.income
        debt_effect_value = 1 - company.debt() / company.capital
        volatility_effect_value = 1 - Macrosphere.inflation / 100

        credit_rating = (w1 * age_effect_value +
                         w2 * profitability_effect_value +
                         w3 * debt_effect_value +
                         w4 * volatility_effect_value)
        return credit_rating


class company:
    def __init__(self):
        self.employment_rate = random.randint(50, 100) / 100
        self.age = random.randint(0, 10)
        self.size = random.randint(1, 15) * 100
        self.capital = random.randint(5, 10) * 100 * 1000
        self.balance = 0
        self.innovation = random.randint(0, 100)/100  # "Айтишность" компании
        self.credits = []
        self.id = len(Macrosphere.company_List)

        # self.credit_rating = rating  # Кредитный рейтинг
        self.income = self.calculate_income()  # Годовой доход
        self.rating = None
        self.last_rating_year = 0  # день когда последний раз проводили оценку

    def debt(self):
        s = 0
        for credit in self.credits:
            s += credit.body
        return s

    def invest(self, investment_sum):
        self.balance -= investment_sum
        increment_inno = (1 / max(self.innovation, 0.01)) * (investment_sum / 1000)
        self.innovation = max(0, min(1, self.innovation + increment_inno))
        increment_emp = (1 / max(self.employment_rate, 0.01)) * (investment_sum / 500)
        self.employment_rate = max(0, min(1, self.employment_rate + increment_emp))

    def calculate_income(self):

        size_factor = math.log(self.size)  # Влияние размера предприятия
        employment_factor = self.employment_rate  # Влияние безработицы
        lamda = 10 - (9 * self.innovation)
        age_factor = 1 - math.exp(-self.age / lamda)  # Вычисление AgeFactor
        debts_interest = 0
        new_cr=[]
        for credit in self.credits:
            debts_interest += (credit.interest_rate / 100 + 1) * credit.body + credit.initial_body/(credit.date_paid-credit.date_given)
            credit.body -= credit.initial_body/(credit.date_paid-credit.date_given)
            if credit.date_paid>=Macrosphere.current_year:
                new_cr.append(credit)
        self.credits=new_cr
        # self.income = self.capital  * (1 + self.innovation) * age_factor - debts_interest - (self.employment_rate * self.size * 1000)
        # Расчет базового дохода
        base_income = self.capital * (1 + self.innovation) * age_factor

        # Вычитаем проценты по долгам
        income_after_debts = base_income - debts_interest

        # Расчет операционных расходов с учетом инноваций
        # Предполагаем, что каждый процент инновации увеличивает стоимость рабочей силы на 2%
        labor_cost_multiplier = 1 + (self.innovation * 2)
        operational_expenses = (self.employment_rate * self.size * 1000) * labor_cost_multiplier

        # Расчет чистого дохода
        self.income = income_after_debts - operational_expenses

        if self.income > 1000:  # Taxes
            Macrosphere.budget += self.income * Macrosphere.tax_rate
            self.income = self.income * (1-Macrosphere.tax_rate)
        # TODO Calculus
        return self.income

    def look_for_credit(self):
        offers = []
        for i, bank in enumerate(Macrosphere.bank_List):
            credit = bank.score_company(self)
            if credit.result:
                offers.append(credit)
        if len(offers):
            best_offer = offers[0]
            for off in offers:
                if off.interest_rate <= best_offer.interest_rate:
                    best_offer = off
            self.balance += best_offer.body
            self.credits.append(best_offer)
            ic(len(self.credits), self.id)
        else:
            self.balance += 1000
            self.employment_rate = (self.employment_rate * self.size - 100) / self.size


if __name__ == '__main__':

    print("Initialisation")
    Macrosphere.initialise()
    print("Initialisation complete")

    # "1" -
    # "2" -
    # "3" -
    #
    Macrosphere.gametype = "1"
    a=0
    while Macrosphere.gameActive:

        Macrosphere.display_macro_factors()
        if a<Macrosphere.current_year:
            a=int(input())

            pass

        Macrosphere.current_year += 1
        Macrosphere.calculus_end_day()

        for i, company in enumerate(Macrosphere.company_List):
            company.calculate_income()
            company.balance += company.income
            company.invest(company.balance / 2)
            if company.balance <= -company.income:
                company.look_for_credit()
                # ic(company)
