import streamlit as st

from utils import stprint


class Expense:
    ID: int = 0

    def __init__(
        self,
        payed_by: str,
        own_shares: int,
        other_shares: dict,
        amount: float,
        note: str,
    ):
        # increment ID
        Expense.ID += 1

        self.payed_by: str = payed_by
        self.own_shares: int = own_shares
        self.other_shares: dict = other_shares
        self.amount: float = amount
        self.ID = Expense.ID
        self.true_shares = self._calc_true_shares()
        self.note = note

    def _calc_true_shares(self) -> list:
        shares_sum = self.own_shares + sum(self.other_shares.values())
        single_share = self.amount / shares_sum
        true_shares = []
        true_shares.append(
            (self.payed_by, self.own_shares, self.own_shares * single_share)
        )
        for name, share in self.other_shares.items():
            true_shares.append((name, share, share * single_share))
        return true_shares

    def __repr__(self) -> str:
        return f"ID: {self.ID}\tPayed by: {self.payed_by}, Own shares: {self.own_shares}, Other shares: {self.other_shares}, Amount: {self.amount}"


class Participant:
    def __init__(self, name: str, shares: int):
        stprint(f"Participant {name} created")
        self.name: str = name
        self.shares: int = shares
        self.expenses: list[Expense] = []

        # a positive amount means the participant gets money from the other participant
        self.dept_book: dict = {}

    def add_expense(self, expense: Expense):
        # this participant payed money
        self.expenses.append(expense)

        true_shares = expense.true_shares
        # stprint(true_shares)
        # other participants owe money
        for name, _, amount in true_shares:
            if name == self.name:
                continue
            if name not in self.dept_book:
                self.dept_book[name] = 0
            self.dept_book[name] += amount

    def participate_in_expense(self, expense: Expense):
        # this participant owes money
        true_shares = expense.true_shares

        # in true_shares are the exact amounts of money
        # all other participants owe to the payed_by participant
        for name, _, amount in true_shares:
            if name == self.name:
                if expense.payed_by not in self.dept_book:
                    self.dept_book[expense.payed_by] = 0
                self.dept_book[expense.payed_by] -= amount
                break

    def remove_expense_payment(self, ID: int):
        stprint(f"Remove expense payment for participant {self.name}")
        target_expense = [expense for expense in self.expenses if expense.ID == ID][0]
        for name, _, amount in target_expense.true_shares:
            if name == self.name:
                continue
            else:
                self.dept_book[name] -= amount

        # remove the expense from the list
        self.expenses = [expense for expense in self.expenses if expense.ID != ID]

    def remove_expense_participation(self, target_expense: Expense):
        stprint(f"Remove expense participation for participant {self.name}")
        for name, _, amount in target_expense.true_shares:
            if name == self.name:
                self.dept_book[target_expense.payed_by] += amount

    def __repr__(self) -> str:
        return f"Name: {self.name}, Dept book: {self.dept_book}"


class Group:
    def __init__(self):
        self.participants: list[Participant] = []

    def add_participant(self, name: str, shares: int):
        participant_exists = self._check_participant_existence(name)
        if participant_exists:
            st.toast(f"Teilnehmer {name} existiert bereits.")
        else:
            # Add participant to the list
            self.participants.append(Participant(name, shares))

    def remove_participant(self, name: str):
        self.participants = [p for p in self.participants if p.name != name]

    def get_shares_by_name(self, name: str):
        for participant in self.participants:
            if participant.name == name:
                return participant.shares
        raise ValueError("Participant not found")

    def add_expense_to_participants(self, payed_by_name: str, expense: Expense):
        for participant in self.participants:
            if participant.name == payed_by_name:
                participant.add_expense(expense)
            else:
                participant.participate_in_expense(expense)

    def pay_dept(self, name: str, other_name: str):
        """
        name: participant who has to give money
        other_name: participant who gets money
        """
        for participant in self.participants:
            if participant.name == name:
                participant.dept_book[other_name] = 0
                for other_participant in self.participants:
                    if other_participant.name == other_name:
                        other_participant.dept_book[name] = 0
                        break
                break

    def remove_expense(self, expense_id: int):
        # get the target_expense from the payed_by participant
        for participant in self.participants:
            for expense in participant.expenses:
                if expense.ID == expense_id:
                    target_expense = expense
                    break

        for participant in self.participants:
            if participant.name == target_expense.payed_by:
                # this participant payed
                participant.remove_expense_payment(expense_id)
            elif participant.name in target_expense.other_shares:
                # this participant owes money
                participant.remove_expense_participation(target_expense)

    def show_all_participants(self):
        for participant in self.participants:
            stprint(participant)

    @property
    def names(self):
        return [participant.name for participant in self.participants]

    @property
    def has_participants(self):
        return len(self.participants) > 0

    @property
    def all_expenses(self):
        expenses = []
        for participant in self.participants:
            expenses.extend(participant.expenses)
        return expenses

    def _check_participant_existence(self, name: str):
        for participant in self.participants:
            if participant.name == name:
                stprint("Participant already exists")
                return True
        return False
