import requests
from bs4 import BeautifulSoup
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

knownData = []
dp = Dispatcher()

def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)

async def get_page_data(bot: Bot):
    url = 'https://lun.ua/uk/search?currency=UAH&geo_id=10009580&has_eoselia=false&is_without_fee=false&price_max=13000&price_sqm_currency=UAH&section_id=2&sort=insert_time&sub_geo_id=10026629'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    announcement = soup.find_all('div', class_='feed-layout__item-container')
    for i in announcement:
        adress = i.find('button', class_='realty-link-button realty-preview-title__link')
        price = i.find('div', class_='realty-preview-price--main')
        description = i.find('p', class_='realty-preview-description__text')

        result = list(filter(lambda x: x['description'] == description, knownData))
        if result:
            continue
        else:
            if price and adress and description:
                print(price.text.strip())
                print(adress.text.strip())
                print(description.text.strip())
                print('\n')
                knownData.append({
                    "description": description,
                    "adress": adress,
                    "price": price
                })
                await bot.send_message(
                    952649628,
                    f"❗❗❗❗❗❗❗❗❗\n```{adress.text.strip()}```\n```{price.text.strip()}```\n```{description.text.strip()}```\n❗❗❗❗❗❗❗❗❗",
                    parse_mode="MarkdownV2"
                 )


async def repeated_task(bot: Bot):
    while True:
        await get_page_data(bot)
        await asyncio.sleep(600)

async def main() -> None:
    bot = Bot(token="", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.create_task(repeated_task(bot))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
