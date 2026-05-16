
from .core.logger import Logger

print(__name__, __file__)
logger = Logger(__name__)

logger.info("This is a test")

def this_test():
    return "This is a test"



if __name__ == "__main__":
    print(this_test())