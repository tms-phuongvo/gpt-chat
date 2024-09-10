import random
import pandas as pd

# Define sample data for Products/Services, Main Clients, and Certifications
products_services = {
    "Cosmetics": [
        "Skincare",
        "Makeup",
        "Personal Care Products",
        "Fragrances",
        "Hair Care",
    ],
    "Fashion": ["Clothing", "Footwear", "Accessories", "Luxury Bags", "Sportswear"],
    "Electronics": [
        "Smartphones",
        "Laptops",
        "Wearable Devices",
        "Consumer Electronics",
        "Home Appliances",
    ],
}

countries_cities = [
    "Hà Nội",
    "Hồ Chí Minh",
    "Đà Nẵng",
    "Hải Phòng",
    "Cần Thơ",
    "Nha Trang",
    "Buôn Ma Thuột",
    "Vũng Tàu",
    "Quy Nhơn",
    "Thái Nguyên",
    "Nam Định",
    "Đồng Nai",
    "Bà Rịa - Vũng Tàu",
    "Hưng Yên",
    "Phú Thọ",
    "Ninh Bình",
    "Bắc Ninh",
    "Thừa Thiên - Huế",
    "Khánh Hòa",
    "Gia Lai",
    "Kon Tum",
    "Lâm Đồng",
    "Sóc Trăng",
    "Trà Vinh",
    "Kiên Giang",
    "Hà Tĩnh",
    "Quảng Bình",
    "Quảng Trị",
    "Lạng Sơn",
    "Cao Bằng",
    "Điện Biên",
    "Hà Giang",
    "Yên Bái",
    "Tuyên Quang",
    "Sơn La",
    "Hòa Bình",
    "Thanh Hóa",
    "Nghệ An",
    "Hà Nam",
    "Hải Dương",
    "Bắc Giang",
    "Nam Định",
    "Ninh Bình",
    "Vĩnh Phúc",
    "Bắc Ninh",
    "Đắk Lắk",
    "Đắk Nông",
    "Lào Cai",
    "Hà Tĩnh",
    "Quảng Ngãi",
    "Bình Định",
    "Phú Yên",
    "Bình Dương",
    "Đồng Tháp",
    "An Giang",
    "Hậu Giang",
    "Bến Tre",
    "Tiền Giang",
    "Long An",
    "Trà Vinh",
    "Sóc Trăng",
    "Cà Mau",
]


main_clients = ["Brand A", "Brand B", "Brand C", "Brand D", "Brand E"]
certifications = [
    "ISO 9001",
    "ISO 14001",
    "GMP Certified",
    "CE Marking",
    "RoHS Compliant",
]


# Function to create a description for each company
def generate_description(
    company_name, industry, location, year, employees, revenue, products, clients, certs
):
    return (
        f"{company_name} is a renowned OEM in the {industry} industry, based in {location}. "
        f"Founded in {year}, the company specializes in {', '.join(products)}. "
        f"With {employees} employees, {company_name} serves major clients like {', '.join(clients)} "
        f"and has earned certifications such as {', '.join(certs)}. "
        f"The company generates an annual revenue of {revenue:.2f} million USD."
    )


# Generate the OEM company data for Cosmetics, Fashion, and Electronics industries
company_data = {
    "Company Name": [f"OEM Company {i+1}" for i in range(300)],
    "Location": [
        f"{random.choice(cities)}, {country}"
        for country, cities in countries_cities.items()
        for _ in range(30)
    ][:300],
    "Industry": [
        "Cosmetics" if i % 3 == 0 else "Fashion" if i % 3 == 1 else "Electronics"
        for i in range(300)
    ],
    "Founded Year": [random.randint(1950, 2020) for _ in range(300)],
    "Employee Count": [random.randint(50, 10000) for _ in range(300)],
    "Annual Revenue (Million USD)": [random.uniform(10, 5000) for _ in range(300)],
    "Website": [f"https://www.oemcompany{i+1}.com" for i in range(300)],
    "Products/Services": [
        random.sample(products_services[industry], 2)
        for industry in ["Cosmetics", "Fashion", "Electronics"] * 100
    ],
    "Main Clients": [random.sample(main_clients, 3) for _ in range(300)],
    "Certifications": [random.sample(certifications, 2) for _ in range(300)],
}

# Add descriptions to the data
company_data["Description"] = [
    generate_description(
        company_data["Company Name"][i],
        company_data["Industry"][i],
        company_data["Location"][i],
        company_data["Founded Year"][i],
        company_data["Employee Count"][i],
        company_data["Annual Revenue (Million USD)"][i],
        company_data["Products/Services"][i],
        company_data["Main Clients"][i],
        company_data["Certifications"][i],
    )
    for i in range(300)
]

# Create DataFrame
oem_cosmetics_fashion_electronics_df = pd.DataFrame(company_data)

# Save to CSV
file_path_with_descriptions = "./oem_cosmetics_fashion_electronics_companies.csv"
oem_cosmetics_fashion_electronics_df.to_csv(file_path_with_descriptions, index=False)
