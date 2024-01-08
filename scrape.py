import requests
from bs4 import BeautifulSoup
import csv
import sys

url = 'https://www.programme.tv/sudoku/jouer.php?annee_grille=2021&jour_grille=1&niveau_grille=moyen'
mainPage = requests.get(url)

soup = BeautifulSoup(mainPage.content, features="html.parser")


def progressBar(count, total, status=''):
    barLen = 50
    progressLen = int(round(barLen * count / total))

    percents = round(100.0 * count / total, 1)
    bar = '=' * progressLen + '-' * (barLen - progressLen)

    sys.stdout.write('%s[%s%s%s]\r' % (status, bar, percents, '%'))
    sys.stdout.flush()


def scrapeOne(soup):
    # liste des valeurs non-manquantes du sudoku
    sudokuOne = []

    # toutes les lignes de 9 cases du sudoku
    allTr = soup.find_all("tr", class_="gridGame-line")

    # Loop qui append les valeurs non-manquantes et des espaces quand les valeurs sont manquantes
    for tr in allTr:
        tdAll = tr.find_all("td")
        for td in tdAll:

            if td.find("span", class_="gridGame-start") is None:
                sudokuOne.append('')

            elif td.find("span", class_="gridGame-start") is not None:
                sudokuOne.append(td.find("span", class_="gridGame-start").text)

    return sudokuOne


def scrapeAll():
    data = []
    total = 101
    for i in range(1, 101):
        option = i
        url = 'https://www.programme.tv/sudoku/jouer.php?annee_grille=2021&jour_grille=' + str(
            option) + '&niveau_grille=moyen'
        secPage = requests.get(url)
        soup = BeautifulSoup(secPage.content, features="html.parser")

        sudokuOne = scrapeOne(soup)
        data.append(sudokuOne)
        sudokuOne = []

        progressBar(i, total - 1, status='Scrapping de 100 Sudokus : ')

    return data


data = scrapeAll()
with open("sudoku.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
