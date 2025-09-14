# create_sample_products.py
import pandas as pd
import os

def create_sample_products_csv():
    """Create a sample products.csv file with comprehensive skincare products"""
    
    sample_products = [
        {
            'name': 'Gentle Foaming Cleanser',
            'brand': 'CeraVe',
            'category': 'Cleanser',
            'skin_type': 'Normal,Oily,Dry',
            'concerns': 'Daily cleansing,Sensitive skin',
            'price': 12.99,
            'rating': 4.5,
            'description': 'A gentle, non-comedogenic foaming facial cleanser that removes makeup and dirt without over-drying the skin. Contains essential ceramides and hyaluronic acid.',
            'ingredients': 'Ceramides, Hyaluronic Acid, Niacinamide, MVE Technology',
            'purchase_link': 'https://www.cerave.com/skincare/cleansers/foaming-facial-cleanser',
            'image_url': 'https://via.placeholder.com/300x400?text=CeraVe+Cleanser&bg=4A90E2&color=white'
        },
        {
            'name': '2% BHA Liquid Exfoliant',
            'brand': "Paula's Choice",
            'category': 'Treatment',
            'skin_type': 'Oily,Normal',
            'concerns': 'Acne,Blackheads,Large pores,Texture',
            'price': 32.00,
            'rating': 4.7,
            'description': 'Powerful 2% BHA (Salicylic Acid) liquid exfoliant that unclogs pores, reduces blackheads, and smooths skin texture for a clearer complexion.',
            'ingredients': 'Salicylic Acid, Green Tea Extract, Methylpropanediol',
            'purchase_link': 'https://www.paulaschoice.com/skin-perfecting-2pct-bha-liquid-exfoliant/201.html',
            'image_url': 'https://via.placeholder.com/300x400?text=Paula+BHA&bg=E74C3C&color=white'
        },
        {
            'name': 'Hyaluronic Acid 2% + B5',
            'brand': 'The Ordinary',
            'category': 'Serum',
            'skin_type': 'Normal,Dry,Oily',
            'concerns': 'Dehydration,Fine lines,Plumping',
            'price': 8.90,
            'rating': 4.3,
            'description': 'Multi-molecular hyaluronic acid serum for intensive hydration at multiple skin depths. Provides long-lasting moisture retention.',
            'ingredients': 'Sodium Hyaluronate, Hyaluronic Acid, Vitamin B5',
            'purchase_link': 'https://theordinary.com/en-us/hyaluronic-acid-2-b5-serum-30ml',
            'image_url': 'https://via.placeholder.com/300x400?text=TO+Hyaluronic&bg=8E44AD&color=white'
        },
        {
            'name': 'Rapid Wrinkle Repair Retinol',
            'brand': 'Neutrogena',
            'category': 'Treatment',
            'skin_type': 'Normal,Oily',
            'concerns': 'Anti-aging,Acne,Fine lines,Texture',
            'price': 18.99,
            'rating': 4.2,
            'description': 'Anti-aging night treatment with retinol SA to accelerate skin renewal and reduce the appearance of fine lines and wrinkles.',
            'ingredients': 'Retinol SA, Hyaluronic Acid, Glucose Complex',
            'purchase_link': 'https://www.neutrogena.com/products/skincare/rapid-wrinkle-repair',
            'image_url': 'https://via.placeholder.com/300x400?text=Neutrogena+Retinol&bg=F39C12&color=white'
        },
        {
            'name': 'Anthelios Ultra Light SPF 60',
            'brand': 'La Roche-Posay',
            'category': 'Sunscreen',
            'skin_type': 'Normal,Oily,Dry',
            'concerns': 'Sun protection,Daily protection',
            'price': 26.99,
            'rating': 4.6,
            'description': 'Lightweight, non-greasy broad spectrum sunscreen with SPF 60. Fast-absorbing formula with antioxidant protection.',
            'ingredients': 'Avobenzone, Homosalate, Octisalate, Octocrylene, Antioxidants',
            'purchase_link': 'https://www.laroche-posay.us/anthelios-ultra-light-sunscreen-fluid',
            'image_url': 'https://via.placeholder.com/300x400?text=LRP+SPF60&bg=27AE60&color=white'
        },
        {
            'name': 'Moisturizing Cream',
            'brand': 'CeraVe',
            'category': 'Moisturizer',
            'skin_type': 'Dry,Normal',
            'concerns': 'Hydration,Dry skin,Barrier repair',
            'price': 16.99,
            'rating': 4.4,
            'description': 'Rich, non-greasy moisturizer with ceramides and MVE technology for 24-hour hydration and skin barrier restoration.',
            'ingredients': 'Ceramides 1, 3, 6-II, Hyaluronic Acid, MVE Technology',
            'purchase_link': 'https://www.cerave.com/skincare/moisturizers/moisturizing-cream',
            'image_url': 'https://via.placeholder.com/300x400?text=CeraVe+Cream&bg=3498DB&color=white'
        },
        {
            'name': 'Niacinamide 10% + Zinc 1%',
            'brand': 'The Ordinary',
            'category': 'Serum',
            'skin_type': 'Oily,Normal',
            'concerns': 'Acne,Large pores,Oil control,Blemishes',
            'price': 7.90,
            'rating': 4.1,
            'description': 'High-strength niacinamide serum to reduce appearance of skin blemishes and congestion. Controls oil production effectively.',
            'ingredients': 'Niacinamide, Zinc PCA, Tamarindus Indica Seed Gum',
            'purchase_link': 'https://theordinary.com/en-us/niacinamide-10pct-zinc-1pct-serum',
            'image_url': 'https://via.placeholder.com/300x400?text=TO+Niacinamide&bg=9B59B6&color=white'
        },
        {
            'name': 'Hydrating Facial Cleanser',
            'brand': 'CeraVe',
            'category': 'Cleanser',
            'skin_type': 'Dry,Normal',
            'concerns': 'Gentle cleansing,Hydration,Sensitive skin',
            'price': 11.99,
            'rating': 4.6,
            'description': 'Non-foaming cream cleanser that removes dirt and makeup while maintaining the skin\'s natural protective barrier.',
            'ingredients': 'Ceramides, Hyaluronic Acid, MVE Technology',
            'purchase_link': 'https://www.cerave.com/skincare/cleansers/hydrating-facial-cleanser',
            'image_url': 'https://via.placeholder.com/300x400?text=CeraVe+Hydrating&bg=16A085&color=white'
        },
        {
            'name': 'Vitamin C 23% + HA Spheres 2%',
            'brand': 'The Ordinary',
            'category': 'Serum',
            'skin_type': 'Normal,Oily',
            'concerns': 'Anti-aging,Dark spots,Brightening',
            'price': 9.10,
            'rating': 4.0,
            'description': 'High-strength vitamin C serum for advanced signs of aging. Helps brighten skin and reduce dark spots.',
            'ingredients': 'L-Ascorbic Acid, Sodium Hyaluronate Spheres',
            'purchase_link': 'https://theordinary.com/en-us/vitamin-c-23pct-ha-spheres-2pct-serum',
            'image_url': 'https://via.placeholder.com/300x400?text=TO+Vitamin+C&bg=E67E22&color=white'
        },
        {
            'name': 'Oil-Free Acne Wash',
            'brand': 'Neutrogena',
            'category': 'Cleanser',
            'skin_type': 'Oily',
            'concerns': 'Acne,Oil control,Deep cleansing',
            'price': 8.99,
            'rating': 4.3,
            'description': 'Oil-free acne fighting face wash with salicylic acid. Clears breakouts without over-drying skin.',
            'ingredients': 'Salicylic Acid, Glycerin, Cocamidopropyl Betaine',
            'purchase_link': 'https://www.neutrogena.com/products/skincare/oil-free-acne-wash',
            'image_url': 'https://via.placeholder.com/300x400?text=Neutrogena+Acne&bg=C0392B&color=white'
        },
        {
            'name': 'Toleriane Double Repair Moisturizer',
            'brand': 'La Roche-Posay',
            'category': 'Moisturizer',
            'skin_type': 'Normal,Dry,Sensitive',
            'concerns': 'Hydration,Sensitive skin,Barrier repair',
            'price': 19.99,
            'rating': 4.5,
            'description': 'Face moisturizer with ceramides and niacinamide. Restores healthy-looking skin and provides 48-hour hydration.',
            'ingredients': 'Ceramides, Niacinamide, Thermal Spring Water',
            'purchase_link': 'https://www.laroche-posay.us/toleriane-double-repair-face-moisturizer',
            'image_url': 'https://via.placeholder.com/300x400?text=LRP+Moisturizer&bg=2ECC71&color=white'
        },
        {
            'name': 'Retinol 1% in Squalane',
            'brand': 'The Ordinary',
            'category': 'Treatment',
            'skin_type': 'Normal,Dry',
            'concerns': 'Anti-aging,Fine lines,Texture',
            'price': 9.90,
            'rating': 4.2,
            'description': 'High-strength retinol serum in squalane base for advanced signs of aging. Promotes skin renewal and smoothness.',
            'ingredients': 'Retinol, Squalane',
            'purchase_link': 'https://theordinary.com/en-us/retinol-1pct-in-squalane-serum',
            'image_url': 'https://via.placeholder.com/300x400?text=TO+Retinol&bg=8B008B&color=white'
        }
    ]
    
    # Create directory if it doesn't exist
    os.makedirs('data/products', exist_ok=True)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(sample_products)
    csv_path = 'data/products/products.csv'
    df.to_csv(csv_path, index=False)
    
    print(f"✅ Created sample products CSV at: {csv_path}")
    print(f"📦 Generated {len(sample_products)} products")
    print("\nProducts by category:")
    category_counts = df['category'].value_counts()
    for category, count in category_counts.items():
        print(f"  - {category}: {count}")
    
    print(f"\nPrice range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")
    print(f"Average rating: {df['rating'].mean():.2f}")
    
    return csv_path

if __name__ == "__main__":
    create_sample_products_csv()