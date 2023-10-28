from decimal import Decimal


def rating_before(const, score):
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
        return Decimal(const) + ((Decimal(score) - Decimal(975000)) // 250 / 100)
    elif 925000 <= score <= 974999:
        return (Decimal(const) - Decimal(3.0)) + ((Decimal(score) - Decimal(925000)) // (Decimal(500) / Decimal(3)) / 100)
    elif 900000 <= score <= 924999:
        return (Decimal(const) - Decimal(5.0)) + ((Decimal(score) - Decimal(900000)) // 125 / 100)
    elif 800000 <= score <= 899999:
        return (Decimal(const) - Decimal(5.0)) * (Decimal(0.5) + (Decimal(score) - Decimal(800000)) / Decimal(200000))
    elif 500000 <= score <= 799999:
        return (Decimal(const) - Decimal(5.0)) * (Decimal(score) - Decimal(500000)) / 600000
    else:
        return 0


def rating(const, score):
    if score >= 1009000:
        return Decimal(const) + Decimal(2.15)
    elif 1007500 <= score <= 1008999:
        return (Decimal(const) + Decimal(2.0)) + ((Decimal(score) - Decimal(1007500)) / 10000)
    elif 1005000 <= score <= 1007499:
        return (Decimal(const) + Decimal(1.5)) + ((Decimal(score) - Decimal(1005000)) / 5000)
    elif 1000000 <= score <= 1004999:
        return (Decimal(const) + Decimal(1.0)) + ((Decimal(score) - Decimal(1000000)) / 10000)
    elif 990000 <= score <= 999999:
        return (Decimal(const) + Decimal(0.6)) + ((Decimal(score) - Decimal(990000)) / 25000)
    elif 975000 <= score <= 989999:
        return Decimal(const) + ((Decimal(score) - Decimal(975000)) / 25000)
    elif 925000 <= score <= 974999:
        return (Decimal(const) - Decimal(3.0)) + ((Decimal(score) - Decimal(925000)) / (Decimal(50000) / Decimal(3)))
    elif 900000 <= score <= 924999:
        return (Decimal(const) - Decimal(5.0)) + ((Decimal(score) - Decimal(900000)) / 12500)
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


print(f"rating(15.3, 987653) = {rating(15.3, 987653)}")
