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
    payoff = None
    bankrupts_List = []
    totalCreditCount = []

    @staticmethod
    def initialise():
        Macrosphere.totalCreditCount = [0,0]
        Macrosphere.bankrupts_List = []
        Macrosphere.tax_rate = 0.2  # Tax Rate
        Macrosphere.global_unemployment_rate = 0.2  # Уровень безработицы
        Macrosphere.inflation = 10  # Уровень инфляции
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
        # ic(Macrosphere.bank_List)
        # ic(Macrosphere.company_List)
        Macrosphere.gameActive = True

    @staticmethod
    def summarise():
        list_credits = []
        for company in Macrosphere.company_List:
            company.payoff = company.balance + company.innovation * company.capital
            for i in company.credits:
                list_credits.append(i)
        bc = []
        for i in range(len(Macrosphere.bank_List)):
            bc.append(0)
        for cr in list_credits:
            for bank in Macrosphere.bank_List:
                if cr.bank_id == bank.id:
                    bc[bank.id] += cr.body

        for bank in Macrosphere.bank_List:
            bank.payoff = bank.capital - bc[bank.id] - bank.debt
            print(f"Payoff Bank: {bank.id, bank.payoff}")
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
        print(f"Employment : {round(Macrosphere.global_unemployment_rate, 2) * 100}%")
        # print(f"Economic Cycle: {Macrosphere.economic_cycles_s[Macrosphere.economic_cycle_n]}")
        print(f"Inflation : {round(Macrosphere.inflation, 2)}%")
        print(f"Consumer_capacity_rate: {round(Macrosphere.consumer_capacity_rate, 2) * 100}%")

        sum_debt = 0
        s0 = 0
        for i in Macrosphere.company_List:
            sum_debt += i.debt()
            for credit in i.credits:
                if credit.bank_id == 0:
                    s0 += credit.body
        print(f"Borrower sum_debt: {sum_debt}")
        print(f"Borrower sum_debt0  sum_debt1: {s0, sum_debt - s0}")

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
            c.income_history.append(c.income)
            s.append(c.employment_rate)
            # ic(c.employment_rate)
        old_c = Macrosphere.consumer_capacity_rate

        Macrosphere.global_unemployment_rate = sum(s) / len(s)
        Macrosphere.consumer_capacity_rate = max(0.01, min(1, sum(s) / len(s)))
        Macrosphere.inflation = max(0.01,
                                    min(100, Macrosphere.inflation + 0.8 * Macrosphere.consumer_capacity_rate - old_c))


class Credit:
    def __init__(self, body, interest_rate, credit_id, bank_id, company_id, result, period=10):
        self.body = body
        self.initial_body = body
        self.interest_rate = interest_rate
        self.credit_id = credit_id
        self.bank_id = bank_id
        self.company_id = company_id
        self.date_given = Macrosphere.current_year
        self.result = result
        self.date_paid = Macrosphere.current_year + period


class Bank:
    def __init__(self, capital):
        self.capital = capital
        self.debt = capital
        self.company = []
        self.id = len(Macrosphere.bank_List)
        Macrosphere.bank_List.append(self)
        self.payoff = 0

    def determine_interest_rate(self, company):
        # Простая логика определения процентной ставки на основе рейтинга кредитора
        if self.id == 0 and Macrosphere.gametype == "1":
            return 10  # TODO GAME 1
        if self.id == 0 and Macrosphere.gametype == "2":
            return 10
        if self.id == 1 and Macrosphere.gametype == "2" and len(company.income_history)>0:
            company.rating = 500*(company.income-sum(company.income_history)/len(company.income_history))/sum(company.income_history)/len(company.income_history)
            #input(company.rating)
        if company.rating > 750:
            return 5  # Низкий риск, низкая ставка
        elif company.rating > 500:
            return 10  # Средний риск, средняя ставка
        else:
            return 15  # Высокий риск, высокая ставка

    def score_company(self, company):
        company.rating = self.creditScore(company)
        # print(company.rating, company.income)
        Macrosphere.curr_credit_id += 1
        creditOffer = Credit(company.size, self.determine_interest_rate(company), Macrosphere.curr_credit_id,
                             bank_id=self.id, company_id=company.id, result=True)
        return creditOffer

    def creditScore(self, company):
        # Веса для каждого фактора
        w1, w2, w3, w4 = 0.25, 0.25, 0.25, 0.25

        age_effect_value = 1 - math.exp(-company.age / 5)
        profitability_effect_value = sum(company.income_history) / len(company.income_history)
        debt_effect_value = 1 - company.debt() / company.capital
        volatility_effect_value = 1 - Macrosphere.inflation / 100

        #ic(age_effect_value, profitability_effect_value, debt_effect_value, volatility_effect_value)

        credit_rating = (w1 * age_effect_value +
                         w2 * profitability_effect_value +
                         w3 * debt_effect_value +
                         w4 * volatility_effect_value)
        return credit_rating


class company:
    def __init__(self):
        self.employment_rate = random.randint(50, 100) / 100
        self.age = random.randint(1, 10)
        self.size = random.randint(1, 15) * 100
        self.capital = random.randint(5, 10) * 100 * 1000
        self.balance = 0
        self.innovation = random.randint(0, 100) / 100  # "Айтишность" компании
        self.credits = []
        self.id = len(Macrosphere.company_List)
        self.income_history = []

        # self.credit_rating = rating  # Кредитный рейтинг
        self.income = self.calculate_income()  # Годовой доход
        self.rating = None
        self.last_rating_year = 0  # день когда последний раз проводили оценку
        self.payoff = 0

    def debt(self):
        s = 0
        for credit in self.credits:
            s += credit.body
        return s

    def invest(self, investment_sum):
        if (self.balance > investment_sum):
            self.balance -= investment_sum
            increment_inno = (1 / max(self.innovation, 0.01)) * (investment_sum / 1000)
            self.innovation = max(0.01, min(1, self.innovation + increment_inno))
            increment_emp = (1 / max(self.employment_rate, 0.01)) * (investment_sum / 500)
            self.employment_rate = max(0.01, min(1, self.employment_rate + increment_emp))

    def calculate_income(self):

        size_factor = math.log(self.size)  # Влияние размера предприятия
        employment_factor = self.employment_rate  # Влияние безработицы
        lamda = 10 - (9 * self.innovation)
        age_factor = 1 - math.exp(-self.age / lamda)  # Вычисление AgeFactor
        debts_interest = 0
        new_cr = []
        for credit in self.credits:
            debts_interest += (credit.interest_rate / 100 + 1) * credit.body + credit.initial_body / (
                    credit.date_paid - credit.date_given)
            credit.body -= credit.initial_body / (credit.date_paid - credit.date_given)
            for bank in Macrosphere.bank_List:
                if credit.bank_id == bank.id:
                    bank.capital += (credit.interest_rate / 100 + 1) * credit.body + credit.initial_body / (
                            credit.date_paid - credit.date_given)
            if credit.date_paid >= Macrosphere.current_year:
                new_cr.append(credit)
        self.credits = new_cr
        # self.income = self.capital  * (1 + self.innovation) * age_factor - debts_interest - (self.employment_rate * self.size * 1000)
        # Расчет базового дохода
        base_income = self.capital * (1 + self.innovation) * (1 + age_factor) * (1 + (random.randint(0, 10) - 5) / 10)
        # ic(self.capital * (1 + self.innovation) * age_factor)
        # ic(self.capital,self.innovation,age_factor)
        # Вычитаем проценты по долгам
        income_after_debts = base_income - debts_interest

        # Расчет операционных расходов с учетом инноваций
        # Предполагаем, что каждый процент инновации увеличивает стоимость рабочей силы на 2%

        # operational_expenses = (((0.5+self.employment_rate) * math.log(self.size)*40000) * (1 + (self.innovation)))
        operational_expenses = (
                    ((1 + self.employment_rate) * math.pow(math.log(self.size + 1), 1.5) * 70000) * math.exp(
                self.innovation * 0.03))

        # input(vars(self))
        # Расчет чистого дохода
        self.income = income_after_debts - operational_expenses
        # ic(self.income, income_after_debts, operational_expenses)
        if self.income < -10000:
            pass
        # ic(base_income,income_after_debts,operational_expenses)
        if self.income > 1000:  # Taxes
            Macrosphere.budget += self.income * Macrosphere.tax_rate
            self.income = self.income * (1 - Macrosphere.tax_rate)
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
            for bank in Macrosphere.bank_List:
                if best_offer.bank_id == bank.id:
                    bank.capital -= best_offer.body
            self.credits.append(best_offer)
            Macrosphere.totalCreditCount[best_offer.bank_id] += 1
        else:
            self.balance += 7000
            self.capital = -10000


if __name__ == '__main__':

    print("Initialisation")
    Macrosphere.initialise()
    print("Initialisation complete")

    # "1" - Кредитный скоринг против низкой ставки
    # "2" -
    # "3" -
    #
    Macrosphere.gametype = "2"
    a = 0
    while Macrosphere.gameActive:

        Macrosphere.display_macro_factors()
        if not a:
            a = 100  # int(input("Игра до года:"))
        if Macrosphere.current_year > a and a != 0:
            ic(Macrosphere.totalCreditCount)
            Macrosphere.summarise()
            break

        Macrosphere.current_year += 1
        Macrosphere.calculus_end_day()

        for i, company in enumerate(Macrosphere.company_List):
            newl = []
            company.calculate_income()
            company.balance += company.income
            company.invest(10000)
            q = 0
            if company.balance <= -company.income:
                company.look_for_credit()
                if q > 10 and company.balance <= -company.income:
                    company.capital -= 1000
                    company.balance += 700
                    q = 0

            if company.capital >= 0:
                newl.append(company)
            else:
                Macrosphere.bankrupts_List.append(company)

            Macrosphere.company_List = newl

            # ic(company)
