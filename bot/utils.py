from aiogram.dispatcher.filters.state import StatesGroup, State


class Work(StatesGroup):

    Length = State()
    Special_symbol = State()
    Big_symbol = State()
    Numbers = State()
    Small_symbol = State()


if __name__ == '__main__':
    print(Work.all())
