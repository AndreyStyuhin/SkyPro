from src.masks import get_mask_card_number, get_mask_account

def main():
    card_example = 7000792289606361
    account_example = 73654112345678901234

    masked_card = get_mask_card_number(card_example)
    masked_account = get_mask_account(account_example)

    print("Маскированная карта:", masked_card)
    print("Маскированный счёт:", masked_account)

if __name__ == "__main__":
    main()