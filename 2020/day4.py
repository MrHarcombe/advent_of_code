from io import StringIO

test = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

fields = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid")

def valid_byr(value):
    try:
        return 1920 <= int(value) <= 2002
    except:
        return False
    
def valid_iyr(value):
    try:
        return 2010 <= int(value) <= 2020
    except:
        return False
    
def valid_eyr(value):
    try:
        return 2020 <= int(value) <= 2030
    except:
        return False

def valid_hgt(value):
    unit = value[-2:]
    value = value[:-2]
    try:
        if unit == "cm":
            return 150 <= int(value) <= 193
        elif unit == "in":
            return 59 <= int(value) <= 76
        else:
            return False
    except:
        return False
    
def valid_hcl(value):
    if len(value) == 7 and value[0] == "#":
        try:
            int(value[1:], 16)
            return True
        except:
            return False
    else:
        return False
    
def valid_ecl(value):
    return value in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")

def valid_pid(value):
    return len(value) == 9 and value.isdigit()

def validate_passport(fields):
    return all((valid_byr(fields["byr"]),
               valid_iyr(fields["iyr"]),
               valid_eyr(fields["eyr"]),
               valid_hgt(fields["hgt"]),
               valid_hcl(fields["hcl"]),
               valid_ecl(fields["ecl"]),
               valid_pid(fields["pid"])))

valid_passports = 0
validated_passports = 0
# with StringIO(test) as data:
with open("input4.txt") as data:
    current = {}
    for line in data:
        line = line.strip()
        if line == "":
            if len(current) == 8 or ("cid" not in current and len(current) == 7):
                valid_passports += 1
                if validate_passport(current):
                    validated_passports += 1
            current = {}

        else:
            for section in line.split():
                for field in fields:
                    if section.startswith(field):
                        field, value = section.split(":")
                        current[field] = value

    
    if len(current) == 8 or ("cid" not in current and len(current) == 7):
        valid_passports += 1
        if validate_passport(current):
            validated_passports += 1

print("Part 1:", valid_passports)
print("Part 1:", validated_passports)
