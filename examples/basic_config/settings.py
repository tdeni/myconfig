from myconfig import MyConfig

config = MyConfig(['settings.toml', '.secrets.toml'])

print(config.some_text)
print(config.some_secrets_text)
print(config.some_text_env)
