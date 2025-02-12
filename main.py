from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date


def main():
    card_example = 7000792289606361
    account_example = 73654112345678901234
    account_card_example = "Счет 73654108430135874305"


    masked_card = get_mask_card_number(card_example)
    masked_account = get_mask_account(account_example)
    transaction_date = "2024-03-11T02:26:18.671407"

    print("Маскированная карта:", masked_card)
    print("Маскированный счёт:", masked_account)
    print(mask_account_card(account_card_example))
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Maestro 7000792289606361"))
    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 64686473678894779589"))
    print(mask_account_card("MasterCard 7158300734726758"))
    print(mask_account_card("Счет 35383033474447895560"))
    print(mask_account_card("Visa Classic 6831982476737658"))
    print(mask_account_card("Visa Platinum 8990922113665229"))
    print(mask_account_card("Visa Gold 5999414228426353"))
    print(get_date(transaction_date))


if __name__ == "__main__":
    main()