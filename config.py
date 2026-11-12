from environs import Env

env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = [int(x) for x in env.list("ADMINS")]
ADMINSTWO = env.int("ADMINSTWO")
ADMINS.append(ADMINSTWO)
devv = env.str("dev")
FILMSDATAURL = env.str("FILMSDATAURL")
FILMSDATAID = env.str("FILMSDATAID")
BOTUSERNAME = env.str("BOTUSERNAME")