from bs4 import BeautifulSoup
import requests
import csv
import openpyxl


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    return None

def get_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    main = soup.find('div', class_="comp mntl-search-results mntl-block")
    pages = main.find('ol', class_="comp mntl-pagination")
    page = pages.find_all('li', class_="mntl-pagination__item")
    for p in page:
        link = p.find('a', class_="button--outlined-little-round type--rabbit-bold").get('href')
        links.append(link)
    return links

        
def get_link_of_food(html):
    soup = BeautifulSoup(html, "html.parser")
    links_food = []
    main = soup.find('div', class_="comp mntl-search-results mntl-block")
    links_specific_food = main.find_all('a', class_="comp mntl-card-list-items mntl-document-card mntl-card card card--no-image")
    for foodl in links_specific_food:
        meal = foodl.get('href')
        links_food.append(meal)
    return links_food
    
def get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find('article', class_="comp allrecipes-article mntl-article mntl-article--two-column-right-rail sc-ad-container adjusted-right-rail")
    title = main.find('h1', class_="article-heading type--lion").text ###################### title
    rating = main.find('div', class_="comp mm-recipes-review-bar__rating mntl-text-block type--squirrel-bold").text ###################### rating
    rating_count = main.find('div', class_="comp mm-recipes-review-bar__rating-count mntl-text-block type--squirrel").text ###################### rating count
    description = main.find('p', class_="article-subheading type--dog").text ###################### description
    details = main.find('div', class_="mm-recipes-details__content").text ###################### details
    ingredients = main.find('ul', class_="mm-recipes-structured-ingredients__list").text
    direction = main.find('ol', class_="comp mntl-sc-block mntl-sc-block-startgroup mntl-sc-block-group--OL").text
    chef = main.find('div', class_="comp mntl-bylines__item mntl-attribution__item mntl-attribution__item--has-date").text ###################### chef
    # nutrition_fact = main.find('tbody', class_="mm-recipes-nutrition-facts-summary__table-body").text ###################### nutrition_facts
    nutrition_fact_element = main.find('div', class_="comp mm-recipes-nutrition-facts-summary")
    if nutrition_fact_element:
        nutrition_fact = nutrition_fact_element.text
    else:
        nutrition_fact = "Nutrition facts not found"


    
    
    data = {
        'title' : title,
        'rating' : rating,
        'rating_count' : rating_count,
        'description' : description,
        'details' : details,
        'ingredients' : ingredients,
        'directions' : direction,
        'chef' : chef,
        'nutrition_facts' : nutrition_fact
    }

    return data

def save_to_excel(data):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = 'Name'
    sheet['B1'] = 'rating'
    sheet['C1'] = 'amount of ratings'
    sheet['D1'] = 'short description'
    sheet['E1'] = 'details'
    sheet['F1'] = 'ingredients'
    sheet['G1'] =  'directions'
    sheet['H1'] =  'author'
    sheet['I1'] =  'nutrition facts'

    for i,item in enumerate(data, start=2):
        sheet[f'A{i}'] = item['title']
        sheet[f'B{i}'] = item['rating']
        sheet[f'C{i}'] = item['rating_count']
        sheet[f'D{i}'] = item['description']
        sheet[f'E{i}'] = item['details']
        sheet[f'F{i}'] = item['ingredients']
        sheet[f'G{i}'] = item['directions']
        sheet[f'H{i}'] = item['chef']
        sheet[f'I{i}'] = item['nutrition_facts']


    wb.save('chicken_dinner_recipes.xlsx')
    

import csv

def save_to_csv(data):
    file = open('chicken_dinner_recipes.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(['Name', 'Rating', 'Amount of Ratings', 'Short Description', 
                     'Details', 'Ingredients', 'Directions','Author', 'Nutrition facts'])
    for item in data:
        writer.writerow([item['title'], item['rating'], item['rating_count'], 
                         item['description'], item['details'], 
                         item['ingredients'], item['directions'],item['chef'] , item['nutrition_facts']]) 

def main():
    URL = 'https://www.allrecipes.com/search?Chicken=Chicken&offset=0&q=Chicken'
    html = get_html(URL)
    page_links = get_links(html)
    data = []
    for p in page_links:
        detail_html = get_html(p)
        food_links = get_link_of_food(detail_html)
        for food_link in food_links:
            food_html = get_html(food_link)
            data.append(get_data(food_html))
    save_to_excel(data)
    save_to_csv(data)

if __name__ == "__main__":
    main()