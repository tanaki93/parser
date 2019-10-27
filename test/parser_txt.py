import json


def main():
    json_data = []
    with open('useragents.txt', 'r') as outfile:
        for i in outfile:
            json_data.append(i.strip())
    with open('useragents.json', 'w') as outfile:
        json.dump(json_data, outfile)


if __name__ == '__main__':
    main()