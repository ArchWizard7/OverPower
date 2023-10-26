from decimal import Decimal


def rating_before(const, score):
    if score >= 1009000:
        return const + 2.15
    elif 1007500 <= score <= 1008999:
        return (const + 2.0) + ((score - 1007500) // 100 / 100)
    elif 1005000 <= score <= 1007499:
        return (const + 1.5) + ((score - 1005000) // 50 / 100)
    elif 1000000 <= score <= 1004999:
        return (const + 1.0) + ((score - 1000000) // 100 / 100)
    elif 990000 <= score <= 999999:
        return (const + 0.6) + ((score - 990000) // 250 / 100)
    elif 975000 <= score <= 989999:
        return const + ((score - 975000) // 250 / 100)
    elif 925000 <= score <= 974999:
        return (const - 3.0) + ((score - 925000) // (5000 / 3) / 100)
    elif 900000 <= score <= 924999:
        return (const - 5.0) + ((score - 900000) // 125 / 100)
    elif 800000 <= score <= 899999:
        return (const - 5.0) * (0.5 + (score - 800000) / 200000)
    elif 500000 <= score <= 799999:
        return (const - 5.0) * (score - 500000) / 600000
    else:
        return 0


def rating(const, score):
    if score >= 1009000:
        return Decimal(const) + Decimal(2.15)
    elif 1007500 <= score <= 1008999:
        return (Decimal(const) + Decimal(2.0)) + ((Decimal(score) - Decimal(1007500)) // 100 / 100)
    elif 1005000 <= score <= 1007499:
        return (Decimal(const) + Decimal(1.5)) + ((Decimal(score) - Decimal(1005000)) // 50 / 100)
    elif 1000000 <= score <= 1004999:
        return (Decimal(const) + Decimal(1.0)) + ((Decimal(score) - Decimal(1000000)) // 100 / 100)
    elif 990000 <= score <= 999999:
        return (Decimal(const) + Decimal(0.6)) + ((Decimal(score) - Decimal(990000)) // 250 / 100)
    elif 975000 <= score <= 989999:
        return Decimal(const) + ((score - 975000) // 250 / 100)
    elif 925000 <= score <= 974999:
        return (Decimal(const) - Decimal(3.0)) + ((Decimal(score) - Decimal(925000)) // (Decimal(5000) / Decimal(3)) / 100)
    elif 900000 <= score <= 924999:
        return (Decimal(const) - Decimal(5.0)) + ((Decimal(score) - Decimal(900000)) // 125 / 100)
    elif 800000 <= score <= 899999:
        return (Decimal(const) - Decimal(5.0)) * (Decimal(0.5) + (Decimal(score) - Decimal(800000)) / Decimal(200000))
    elif 500000 <= score <= 799999:
        return (Decimal(const) - Decimal(5.0)) * (Decimal(score) - Decimal(500000)) / 600000
    else:
        return 0


def difficulty_format(diff):
    if (diff * 10) % 10 >= 5:
        return f"{int(diff)}+"
    else:
        return f"{int(diff)}"


# for i in range(0, 101):
#     score = 1000000 + (i * 100)
#     print(f"15.0, {score} = {round(rating(15.0, score), 3)}")


for i in range(100, 155):
    const = i / 10
    print(f"{const} => {difficulty_format(const)}")
