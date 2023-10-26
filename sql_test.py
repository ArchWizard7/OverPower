def rating(const, score):
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


print(rating(14.9, 1010000))
print(rating(14.9, 1009200))
print(rating(14.9, 1009000))
print(rating(14.9, 1008800))
print(rating(14.9, 1007500))
print(rating(14.9, 1005000))
print(rating(14.9, 1000000))
print(rating(14.9, 990000))
print(rating(14.9, 975000))
print(rating(14.9, 925000))
print(rating(14.9, 900000))
print(rating(14.9, 800000))
print(rating(14.9, 500000))
print(rating(14.9, 0))
