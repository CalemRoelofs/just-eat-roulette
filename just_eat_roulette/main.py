import uvicorn  # type: ignore


def main():
    uvicorn.run("just_eat_roulette.server.server:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
