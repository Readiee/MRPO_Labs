import asyncio

class User:
    def __init__(self):
        self.state = 'Оффлайн'

    async def enter_app(self):
        print("Пользователь вошел в приложение")
        self.state = 'Онлайн'
        await asyncio.sleep(1)

    async def exit_app(self):
        print("Пользователь вышел из приложения")
        self.state = 'Оффлайн'
        await asyncio.sleep(1)

    async def display_state(self):
        while True:
            print(f"Пользователь - {self.state}")
            await asyncio.sleep(1)

async def main():
    user = User()
    tasks = [user.enter_app(), user.display_state(), user.exit_app(), user.display_state(), user.enter_app()]  # Создание списка задач

    # Запуск задач и ожидание их завершения
    await asyncio.gather(*tasks)

# Создание цикла событий и запуск функции main()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
