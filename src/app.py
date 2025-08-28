# import time
# from controllers import ProjectsController

# class Application:
#     def __init__(self):
#         self.projects_controller = ProjectsController()

#     def main(self):
#         self.projects_controller.update_address("370")

# if __name__ == "__main__":
#     while True:
#         try:
#             Application().main()
#             break
#         except Exception as e:
#             print(f"Error: {e}")
#             print("Restarting application in 5 seconds...\n")
#             time.sleep(5)


import asyncio
import time
from controllers import ProjectsController
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class Application:
    def __init__(self):
        self.projects_controller = ProjectsController()

    async def main(self):
        start_time = time.time()
        logging.info("Iniciando atualização de projetos...")

        results = await self.projects_controller.get_projects()

        total = len(results)
        success = sum(1 for r in results if r["status"] == "success")
        failed = total - success

        logging.info(f"Processamento finalizado: {total} projetos ({success} success / {failed} failed)")
        logging.info(f"Execução total em {time.time() - start_time:.2f} segundos.")

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(Application().main())
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Restarting application in 5 seconds...\n")
            time.sleep(5)
