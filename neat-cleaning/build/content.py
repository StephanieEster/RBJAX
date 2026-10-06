"""Content for the Neat Cleaning website: business facts, services, FAQs and legal text.

Only facts supplied by the business are stated here (no invented prices, reviews,
licenses or insurance). Edit this file to change copy, then run build.py.
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------- business data
PHONE = '(508) 202-8132'
PHONE_E164 = '+15082028132'
SMS = 'sms:+15082028132'
TEL = 'tel:+15082028132'
EMAIL = 'Neatcleaningservicesusa@gmail.com'
OWNER = 'Daiane Ventura de Oliveira Hotis'
UPDATED = 'October 2026'
UPDATED_ISO = '2026-10-06'
ORIGIN = '{{ORIGIN}}'  # replaced by render-page.php with the live https origin
BIZ_ID = ORIGIN + '/#business'
SITE_ID = ORIGIN + '/#website'
NATICK = (42.2834, -71.3495)

SERVICES = [
    # slug, name, short, nav blurb, best for, hero image, detail image, preview caption
    dict(slug='regular-cleaning', icon='home', name='Regular Cleaning', short='Regular cleaning',
         blurb='Recurring visits that keep a lived-in home in order.',
         fit='Homes that are mostly in order and need steady upkeep.',
         hero='regular-hero', detail='regular-detail', core=True),
    dict(slug='deep-cleaning', icon='sparkles', name='Deep Cleaning', short='Deep cleaning',
         blurb='A detailed reset for build-up that routine upkeep misses.',
         fit='First visits, long gaps between cleans, a start before regular care.',
         hero='deep-hero', detail='deep-detail', core=True),
    dict(slug='airbnb-cleaning', icon='key', name='Airbnb Cleaning', short='Airbnb cleaning',
         blurb='Turnovers planned around check-out and check-in.',
         fit='Short-term rental hosts within 25 miles of Natick.',
         hero='airbnb-hero', detail='airbnb-detail', core=False),
    dict(slug='move-in-move-out-cleaning', icon='truck', name='Move-In & Move-Out', short='Move-in & move-out cleaning',
         blurb='One clean for the home you are leaving or moving into.',
         fit='Tenants, owners and landlords between occupants.',
         hero='move-hero', detail='move-detail', core=False),
    dict(slug='commercial-cleaning', icon='building', name='Commercial Cleaning', short='Commercial cleaning',
         blurb='Offices and workspaces, with timing agreed in advance.',
         fit='Local offices, reception areas and shared workspaces.',
         hero='commercial-hero', detail='commercial-detail', core=False),
]
SVC = {s['slug']: s for s in SERVICES}

IMG_ALT = {
    'home-hero': 'Bright living room with linen sofas, fireplace and oak coffee table',
    'home-kitchen': 'Cream kitchen with marble island, brass pendant lights and wood stools',
    'regular-hero': 'Living room with sofa, armchair and fireplace in soft afternoon light',
    'regular-detail': 'Round dining table with wishbone chairs beside tall windows',
    'deep-hero': 'Blue-grey kitchen with marble island, brass pendants and range hood',
    'deep-detail': 'Open oven with clean racks in a white kitchen',
    'airbnb-hero': 'Guest bedroom with made bed, wool throw and bedside lamps',
    'airbnb-detail': 'Open-plan living area and kitchen ready for the next guest',
    'move-hero': 'Empty entry hall with wood floors and a white staircase',
    'move-detail': 'Empty kitchen with island, stainless refrigerator and stone floor',
    'commercial-hero': 'Office with glass partitions, desks and task chairs',
    'commercial-detail': 'Reception lounge with armchairs and a wood front desk',
    'about-hero': 'Dining room with long wood table, rush chairs and a chandelier',
    'contact-hero': 'Front entry with bench, open door and a view to the garden',
    'area-hero': 'Colonial houses on a tree-lined Massachusetts street in autumn',
}

TOWNS = {
    'Wellesley': (42.2968, -71.2924), 'Sherborn': (42.2390, -71.3698), 'Framingham': (42.2793, -71.4162),
    'Dover': (42.2459, -71.2828), 'Wayland': (42.3626, -71.3614), 'Needham': (42.2809, -71.2378),
    'Ashland': (42.2612, -71.4634), 'Weston': (42.3668, -71.3031), 'Holliston': (42.2001, -71.4245),
    'Medfield': (42.1876, -71.3064), 'Sudbury': (42.3834, -71.4162), 'Westwood': (42.2140, -71.2245),
    'Millis': (42.1676, -71.3579), 'Newton': (42.3370, -71.2092), 'Waltham': (42.3765, -71.2356),
    'Southborough': (42.3057, -71.5245), 'Hopkinton': (42.2287, -71.5226), 'Dedham': (42.2418, -71.1662),
    'Norwood': (42.1945, -71.1995), 'Medway': (42.1418, -71.3967), 'Lincoln': (42.4259, -71.3040),
    'Watertown': (42.3709, -71.1828), 'Marlborough': (42.3459, -71.5523), 'Brookline': (42.3318, -71.1212),
    'Concord': (42.4604, -71.3489), 'Lexington': (42.4473, -71.2245), 'Milford': (42.1398, -71.5162),
    'Westborough': (42.2695, -71.6162), 'Franklin': (42.0834, -71.3967),
}


def miles(a, b):
    r = 3958.8
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def bearing(a, b):
    dx = (b[1] - a[1]) * math.cos(math.radians(a[0]))
    dy = b[0] - a[0]
    ang = (math.degrees(math.atan2(dx, dy)) + 360) % 360
    return ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest'][round(ang / 45) % 8]


TOWN_LIST = sorted(((t, miles(NATICK, c), bearing(NATICK, c)) for t, c in TOWNS.items()), key=lambda x: x[1])
DIST = {t: d for t, d, _ in TOWN_LIST}


# ---------------------------------------------------------------- FAQ content
FAQ_GENERAL = {
    'Booking & quotes': [
        ('How do I get a cleaning quote?', f'Text {PHONE} or send the quote form with your name, phone, email, service and town or ZIP code. Daiane replies by text to go over your home, the areas that matter most, pets and access. Price, scope and timing are confirmed with you before anything is booked, so the quote reflects your actual home rather than a generic package.'),
        ('How much does house cleaning cost?', 'Neat Cleaning quotes each home individually instead of publishing a flat rate. The main factors are the size of the home, the service you choose, how often you want visits, its current condition and special requests such as specific products. Share those details by text or in the form and you receive a quote before booking. Ask about the 10% off offer at the same time.'),
        ('What cleaning services do you offer?', 'Neat Cleaning offers regular cleaning, deep cleaning, Airbnb and short-term rental cleaning, move-in and move-out cleaning, and commercial cleaning for local workspaces. Regular and deep cleaning are the main focus. If you are unsure which fits, describe your home and when it was last professionally cleaned, and Daiane will suggest where to start.'),
        ('How far from Natick do you travel?', 'Neat Cleaning is based in Natick, Massachusetts, and serves locations up to 25 miles away. That radius includes towns such as Framingham, Wellesley, Needham, Wayland, Sudbury, Holliston and Newton. Availability depends on your exact location and the schedule, so send your town or ZIP code and we will confirm before you book.'),
        ('What happens after I send the form?', 'Your request goes to Neat Cleaning with the service, town and details you shared. You are contacted by text or phone at the number you provided to talk through the scope and confirm your quote. Sending the form is an inquiry, not a booking: nothing is scheduled until you agree to the price and timing.'),
        ('Can I change my appointment?', f'Yes. Text {PHONE} as soon as you know you need a change. The sooner you reach out, the easier it is to find another time that works. New availability and any arrangements related to the change are confirmed directly with you by text, so you always know where your appointment stands.'),
    ],
    'During the visit': [
        ('Who will clean my home?', f'Neat Cleaning is led by {OWNER}, who takes care of the cleaning herself. When demand requires it, additional help is arranged. You talk with Daiane directly by text before the visit, so the preferences you share are heard by the person responsible for the cleaning.'),
        ('Do you bring your own cleaning products?', 'Yes. Neat Cleaning brings its own products to every visit, so you do not need to stock anything. If you prefer a specific product, for example because of allergies, pets or surfaces that need special care, tell us before booking. Special product requests are discussed in advance and may affect the quote.'),
        ('Are the oven and refrigerator an extra charge?', 'No. Oven and refrigerator cleaning are included without a separate extra charge, where many services sell them as add-ons. Mention them when you request your quote so access and preparation can be planned, including how full the refrigerator will be on the day of the visit.'),
        ('Can you use products I provide?', 'Yes, specific product requests can be discussed in advance. Neat usually brings its own products, but if you would like something particular used in your home, mention it when you request your quote. Exceptions to the usual products may affect the quote, and everything is confirmed with you before the appointment is booked.'),
        ('What if I have a pet at home?', 'Mention your pets before booking, along with any product concerns and the rooms they use most. We will discuss access and the preferences you would like considered on the day. Letting us know in advance helps the visit go smoothly for you, your pet and the cleaning itself.'),
    ],
    'Payment & offer': [
        ('What payment methods do you accept?', f'Neat Cleaning accepts Zelle, cash and check. Payment details are confirmed directly when your appointment is arranged, so you know how and when to pay before the visit. If you have a question about paying for recurring visits or for a commercial space, text {PHONE}.'),
        ('How does the 10% off offer work?', 'Mention the 10% off offer by text or in the details field of the quote form. Daiane confirms how it applies to your booking before you agree to the service, so there is no guesswork about the final amount. The offer is applied according to what is confirmed for your appointment.'),
    ],
    'Text messages': [
        ('How do I stop text messages?', f'Reply STOP to any message to opt out of texts from Neat Cleaning. You may receive one final message confirming that you have been unsubscribed. Reply HELP for help, or contact Neat Cleaning at {PHONE} or {EMAIL}. Texts that follow a form request are about your request only, not promotions.'),
    ],
}

SERVICE_PAGES = {
    'regular-cleaning': dict(
        title='Regular House Cleaning in Natick, MA | Neat Cleaning',
        desc='Recurring house cleaning in Natick, MA and within 25 miles. Owner-led, own products, oven and fridge included. Text (508) 202-8132 for your quote.',
        h1='Regular house cleaning in Natick, MA',
        kick='Recurring home care',
        lead='Weekly, every-two-week or monthly visits for homes in Natick and the towns around it. You plan the routine with Daiane by text, and the same priorities are followed every time.',
        define='Regular house cleaning is a recurring in-home visit that cleans kitchens, bathrooms, bedrooms, living areas and floors on a set schedule, keeping a Natick-area home at a consistent level between visits.',
        fit_yes=['Your home is in reasonably good shape and you want it kept that way.', 'You want a set rhythm: weekly, every two weeks or monthly.', 'You prefer one person you can text about how your home should be cared for.'],
        fit_no=['It has been months since a professional clean: start with <a class="inline-link" href="/deep-cleaning.html">a deep cleaning visit</a>.', 'You are moving in or out: see <a class="inline-link" href="/move-in-move-out-cleaning.html">cleaning between occupants</a>.'],
        focus_title='Care for the rooms you use every day.',
        focus_text='Regular cleaning is the core of Neat Cleaning. It covers the spaces your household uses daily, and the details that make a home feel looked after again.',
        focus=[('Kitchen and everyday surfaces', 'Counters, fronts and the surfaces you touch most.'), ('Bathrooms and frequently used spaces', 'The rooms that need attention every visit.'), ('Bedrooms and living areas', 'Where the household actually spends its time.'), ('Floors and finishing touches', 'The final pass that makes the home feel finished.'), ('Oven and refrigerator', 'Included without a separate extra charge.')],
        factors=[('Size of the home', 'Bedrooms, bathrooms and living areas set most of the time per visit.'), ('Frequency', 'Weekly, every-two-week and monthly visits are planned differently.'), ('Current condition', 'If there is significant build-up, a deep clean may be suggested first.'), ('Priorities and requests', 'Specific products or focus areas can change the scope.'), ('Pets and access', 'Shared before booking so the visit is planned correctly.')],
        related=f'This page covers recurring visits for a home that is already in good shape. When there is build-up to remove first, <a class="inline-link" href="/deep-cleaning.html">deep cleaning in Natick</a> is the better starting point, and regular visits then keep the result. Hosts preparing a listing between guests should look at <a class="inline-link" href="/airbnb-cleaning.html">turnover cleaning for short-term rentals</a>, and if you are packing up, <a class="inline-link" href="/move-in-move-out-cleaning.html">move-out cleaning</a> is planned around empty rooms and moving dates. Not sure which one fits? <a class="inline-link" href="/services.html">Compare the five services side by side</a>.',
        faqs=[
            ('How often should I schedule regular cleaning?', 'It depends on how the home is used. Many households choose weekly, every two weeks or monthly visits; homes with children, pets or a lot of cooking usually benefit from more frequent care. Tell us your preferred frequency by text or in the quote form, and we will confirm a schedule based on your home and availability.'),
            ('How much does regular cleaning cost in Natick?', f'Regular cleaning is quoted per home. The size of the home, the number of bathrooms, how often you want visits and any special requests set the price. Share those details by text at {PHONE} or in the form on this page and you receive a quote before anything is booked. Mention the 10% off offer when you ask.'),
            ('Should I start with a deep cleaning?', 'If your home has not had professional cleaning in a while, a deep cleaning first is usually the better starting point. It removes the build-up, and regular visits then keep the home at that level. Describe the current condition and we will discuss the scope of the first visit before you commit to a routine.'),
            ('What does a regular cleaning visit focus on?', 'Regular visits focus on the spaces you use every day: the kitchen and everyday surfaces, bathrooms, bedrooms and living areas, and floors with the finishing touches. Oven and refrigerator cleaning are included without extra charge. You can set priorities when you request your quote, and the final scope is confirmed before booking.'),
            ('Do I need to provide cleaning supplies?', 'No. Neat Cleaning brings its own cleaning products to every visit. If you would like a specific product used, because of allergies, pets or delicate surfaces, tell us before booking. Special product requests are discussed in advance and may affect the quote, so the visit is planned with the right supplies from the start.'),
            ('Who cleans my home on each visit?', 'Neat Cleaning is owner-led. Daiane takes care of the cleaning herself, with additional help arranged when demand requires it. The person you text about your preferences is the person responsible for your home, rather than a rotating crew you meet for the first time at the door.'),
            ('Do you offer regular cleaning in towns near Natick?', 'Yes. Regular cleaning is available in Natick and locations up to 25 miles away, including towns such as Framingham, Wellesley, Needham, Sherborn, Wayland and Holliston. Availability depends on your exact location and the schedule, so include your town or ZIP code in your request and we will confirm.'),
        ]),
    'deep-cleaning': dict(
        title='Deep Cleaning in Natick, MA | Home Reset | Neat Cleaning',
        desc='Deep house cleaning in Natick, MA and within 25 miles: kitchens, bathrooms and appliance build-up, oven and fridge included. Text (508) 202-8132 for a quote.',
        h1='Deep cleaning in Natick, MA',
        kick='The detailed reset',
        lead='For build-up that everyday upkeep does not reach. A deep cleaning gives your home a fresh starting point, as a one-time visit or before regular care begins.',
        define='Deep cleaning is a detailed one-time visit that removes build-up in kitchens, bathrooms, appliances and areas routine upkeep misses, giving a home a reset before regular cleaning begins.',
        fit_yes=['Kitchens and bathrooms show build-up that everyday cleaning does not reach.', 'It is your first visit with Neat, or a long time since the last professional clean.', 'You want a solid starting point before switching to regular visits.'],
        fit_no=['Your home is already well kept: <a class="inline-link" href="/regular-cleaning.html">recurring visits</a> will cost you less time and effort.', 'The home will be empty between occupants: see <a class="inline-link" href="/move-in-move-out-cleaning.html">move-in and move-out cleaning</a>.'],
        focus_title='Where a deep clean makes the difference.',
        focus_text='Deep cleaning and regular cleaning work together: a more detailed first visit creates the baseline that ongoing care maintains. Describe the areas you want prioritized so the quote reflects your home.',
        focus=[('Kitchen details and appliance priorities', 'The areas where build-up shows first.'), ('Bathrooms that need extra attention', 'Detail work beyond a routine wipe-down.'), ('Spaces needing more than routine upkeep', 'The rooms you name when you request your quote.'), ('Oven and refrigerator', 'Included without a separate extra charge.'), ('A starting point for regular cleaning', 'Optional: keep the result with recurring visits.')],
        factors=[('Size of the home', 'Bedrooms, bathrooms and living areas set the base time.'), ('Current condition', 'Time since the last professional clean changes the work involved.'), ('Priority areas', 'The rooms and details you want the visit to focus on.'), ('Appliances', 'Oven and refrigerator are included; their condition helps plan the time.'), ('Products, pets and access', 'Special requests are discussed in advance and may affect the quote.')],
        related=f'Deep cleaning is a one-time, detailed reset. Once the build-up is gone, <a class="inline-link" href="/regular-cleaning.html">regular house cleaning</a> keeps the home at that level with less work per visit. If the property is about to be empty, <a class="inline-link" href="/move-in-move-out-cleaning.html">move-out cleaning</a> is planned around moving dates instead, and offices and studios are covered by <a class="inline-link" href="/commercial-cleaning.html">commercial cleaning for workspaces</a>. You can also <a class="inline-link" href="/faq.html">read the common questions about products, payment and timing</a>.',
        faqs=[
            ('What is the difference between deep cleaning and regular cleaning?', 'Regular cleaning maintains a home that is already in good shape. Deep cleaning is a more detailed visit for build-up that everyday upkeep does not reach, in kitchens, bathrooms and areas that need more than routine attention. A common approach is to book a deep clean first, then switch to regular visits to keep the result.'),
            ('Is there a fixed deep cleaning price?', 'No fixed price is published, because deep cleaning depends heavily on the home. Size, number of bathrooms, current condition and the areas you want prioritized all change the time needed. Share those details and you receive a quote for your space, confirmed before booking. Ask about the 10% off offer at the same time.'),
            ('Are oven and refrigerator cleaning extra?', 'No. Neat Cleaning includes oven and refrigerator cleaning without a separate extra charge. Mention them when you request your quote so access and preparation can be planned. Appliances are often where a deep clean makes the most visible difference in a kitchen, so it is worth describing their condition.'),
            ('When does a home need a deep cleaning?', 'Common moments are the first visit with a new cleaner, after a long stretch without professional cleaning, before or after hosting, at the change of seasons and before starting regular service. If surfaces look fine but the kitchen and bathrooms still show build-up, a deep cleaning is usually the right reset.'),
            ('How long does a deep cleaning take?', 'It depends on the size and condition of the home and the areas you prioritize, so timing is discussed when your quote is prepared. A deep cleaning takes longer than a regular visit because it covers more detail. You will know the expected timing before your appointment is confirmed.'),
            ('Can I book a deep cleaning once, without a recurring plan?', 'Yes. Deep cleaning can be booked as a one-time visit. If you later want to keep the home at that level, you can discuss regular cleaning visits; the deep clean then becomes a starting point for ongoing care rather than a commitment you have to make upfront.'),
            ('How should I prepare for a deep cleaning?', 'Tell us about access instructions, pets, product preferences and the rooms that matter most. Clearing countertops and personal items from the areas you want cleaned lets the visit focus on cleaning rather than tidying. Mention the oven and refrigerator so their preparation can be discussed beforehand.'),
        ]),
    'airbnb-cleaning': dict(
        title='Airbnb Cleaning in Natick, MA | Turnovers | Neat Cleaning',
        desc='Airbnb and short-term rental turnover cleaning in Natick, MA and within 25 miles, planned around check-out and check-in. Text (508) 202-8132 for a quote.',
        h1='Airbnb cleaning in Natick, MA',
        kick='Short-term rental turnovers',
        lead='Turnover cleaning planned around your guests’ check-out and check-in, following your listing’s own standards so the next arrival finds the place ready.',
        define='Airbnb cleaning is a turnover service that resets a short-term rental between check-out and check-in, preparing bedrooms, bathrooms and the kitchen to the host’s standard for the next guest.',
        fit_yes=['You host a short-term rental within 25 miles of Natick.', 'You need cleaning planned around check-out and check-in times.', 'You have a checklist or house standards you want followed.'],
        fit_no=['It is your own home on a routine: see <a class="inline-link" href="/regular-cleaning.html">recurring house cleaning</a>.', 'A long-term tenant is leaving: <a class="inline-link" href="/move-in-move-out-cleaning.html">move-out cleaning</a> fits better.'],
        focus_title='Plan the clean around the stay.',
        focus_text='Every rental has its own layout and turnover window. A conversation before the first turnover sets priorities for guest spaces, bathrooms and the kitchen, and confirms availability for your calendar.',
        focus=[('Guest bedrooms and shared spaces', 'Rooms reset to the way your listing presents them.'), ('Kitchen and bathroom priorities', 'The areas guests notice first.'), ('Your property’s cleaning instructions', 'Your checklist, reviewed before the first turnover.'), ('Timing between departures and arrivals', 'Confirmed against your booking calendar.'), ('Laundry, linens and restocking', 'Discussed before booking, never assumed.')],
        factors=[('Size of the rental', 'Bedrooms and bathrooms set the base time per turnover.'), ('Turnover window', 'The time between check-out and check-in affects scheduling.'), ('Frequency of stays', 'How often turnovers happen across the month.'), ('Laundry and restocking', 'Included only when agreed in the confirmed scope.'), ('Location', 'Confirmed within the 25-mile radius together with timing.')],
        related=f'Airbnb cleaning is built around turnover windows and host checklists. If you live in the home and want steady upkeep, <a class="inline-link" href="/regular-cleaning.html">regular cleaning visits</a> are the better match. Before a new listing goes live, or after a long season of bookings, a <a class="inline-link" href="/deep-cleaning.html">detailed deep clean</a> can set the baseline. For towns covered, see <a class="inline-link" href="/service-areas.html">the Natick-area service radius</a>.',
        faqs=[
            ('Can you clean between guest stays?', 'Airbnb cleaning is available by arrangement. Share the guest check-out and check-in times along with your booking calendar so we can confirm whether your turnover window can be accommodated. Turnovers depend on availability, so the earlier your calendar is shared, the easier it is to plan around your bookings.'),
            ('Are laundry and restocking included?', 'Laundry, linens, guest supplies and restocking are discussed before booking rather than assumed. Tell us what your listing needs between stays, and the quote and confirmed scope will state what is included. This keeps expectations clear for you and avoids surprises when the next guest arrives.'),
            ('How is Airbnb cleaning priced?', 'Each property is quoted individually. The size of the rental, the number of bedrooms and bathrooms, how often turnovers happen and any laundry or restocking requests set the price. Share your listing details by text or in the form on this page and you receive a quote before the first turnover is booked.'),
            ('Can I share my own cleaning checklist?', 'Yes, and it is encouraged. Every rental has its own layout and host standards. Share your property’s cleaning instructions, access details and the priorities for guest bedrooms, the kitchen and bathrooms. They are reviewed with you before the first turnover so each visit follows the same standard.'),
            ('Do you clean short-term rentals outside Natick?', 'Yes, within the service radius. Neat Cleaning serves short-term rentals in Natick and locations up to 25 miles away, such as Framingham, Wellesley and Needham. Send the property’s town or ZIP code with your request; location and turnover timing are confirmed together before booking.'),
            ('Do you bring the cleaning products?', 'Yes. Neat Cleaning brings its own cleaning products. If your listing uses specific products, for example fragrance-free options for guests with sensitivities, tell us before booking. Specific product requests are discussed in advance and may affect the quote.'),
        ]),
    'move-in-move-out-cleaning': dict(
        title='Move-In & Move-Out Cleaning in Natick, MA | Neat Cleaning',
        desc='Move-in and move-out cleaning in Natick, MA and within 25 miles. Kitchen, appliances, bathrooms and floors, oven and fridge included. Text for a quote.',
        h1='Move-in &amp; move-out cleaning in Natick, MA',
        kick='Between occupants',
        lead='Moving brings enough to organize. Book one clean for the home you are leaving or the one you are moving into, planned around your dates and access.',
        define='Move-in and move-out cleaning is a one-time clean of a home between occupants, covering the kitchen, appliances, bathrooms, rooms and floors so the property is ready to hand over or move into.',
        fit_yes=['You are leaving a rental or sold home and want it cleaned before handing over the keys.', 'You are moving into a home and want it cleaned before your things arrive.', 'You are a landlord or owner preparing a property between occupants.'],
        fit_no=['You are staying put and want a full reset: book <a class="inline-link" href="/deep-cleaning.html">a deep clean of your home</a>.', 'It is a guest turnover: see <a class="inline-link" href="/airbnb-cleaning.html">Airbnb cleaning</a>.'],
        focus_title='Care for the space between chapters.',
        focus_text='Whether you are preparing a new home or leaving one, the needs are different from an everyday visit. Let us know if the space will be empty, which areas need attention and how access will be coordinated.',
        focus=[('Kitchen and appliance priorities', 'Usually the first thing checked at a handover.'), ('Oven and refrigerator', 'Included without a separate extra charge.'), ('Bathrooms and interior living spaces', 'Every room the next occupant will use.'), ('Empty rooms and accessible floors', 'More surfaces are reachable once furniture is out.'), ('Access and your moving schedule', 'Keys, lockboxes and dates agreed beforehand.')],
        factors=[('Size of the property', 'Bedrooms, bathrooms and living areas set the base time.'), ('Empty or furnished', 'What remains in the rooms changes what can be reached.'), ('Current condition', 'Time since the last thorough clean affects the work.'), ('Date and access', 'Closing, lease and moving dates are confirmed with availability.'), ('Appliances', 'Included; their condition helps plan the visit.')],
        related=f'This page covers homes between occupants. If you are not moving and simply want a thorough reset, <a class="inline-link" href="/deep-cleaning.html">deep house cleaning</a> is the right service, and once you are settled in, <a class="inline-link" href="/regular-cleaning.html">recurring cleaning for your new home</a> keeps it that way. Hosts between guests should see <a class="inline-link" href="/airbnb-cleaning.html">short-term rental turnovers</a>.',
        faqs=[
            ('Does the home need to be empty?', 'Not necessarily. Tell us whether furniture or belongings will still be there on the cleaning day. Empty rooms allow more surfaces and floors to be reached, so the scope changes depending on what remains. We discuss access and the scope with you before confirming your appointment.'),
            ('Can you guarantee my security deposit?', 'No cleaning service can determine a landlord’s deposit decision, so no deposit return is promised. What we can do is go over the property’s cleaning priorities with you, including kitchen, appliances, bathrooms and floors, and agree on the scope before the visit, so you know exactly what will be cleaned before you hand back the keys.'),
            ('Is oven and refrigerator cleaning included in a move-out?', 'Yes. Oven and refrigerator cleaning are included without a separate extra charge. In a move-in or move-out, appliances are often one of the first things checked, so mention their condition when you request your quote and we will plan access and preparation.'),
            ('When should I schedule a move-out cleaning?', 'Ideally after your belongings are out and before the keys are returned or the new occupants arrive. Share your moving schedule, closing or lease dates and access details when you request your quote, and timing is discussed based on availability. Reaching out early gives you more flexibility around moving day.'),
            ('Can a landlord or owner book the cleaning?', 'Yes. Move-in and move-out cleaning is available to tenants, owners and landlords preparing a property between occupants within 25 miles of Natick. Share the property’s town, its condition, whether it will be empty and how access is handled, and scope and timing are confirmed before booking.'),
            ('How is move-in or move-out cleaning priced?', 'Each property is quoted individually. Size, number of bathrooms, current condition, whether the rooms will be empty and the date you need all affect the price. Share those details by text or in the form on this page and you receive a quote before booking. Ask about the 10% off offer when you request it.'),
        ]),
    'commercial-cleaning': dict(
        title='Office & Commercial Cleaning in Natick, MA | Neat Cleaning',
        desc='Office and workspace cleaning in Natick, MA and within 25 miles. Reception, kitchenette and restroom care, timing agreed in advance. Text for a quote.',
        h1='Commercial cleaning in Natick, MA',
        kick='Offices & workspaces',
        lead='Cleaning for local offices and shared workspaces, with the scope, schedule and access agreed in advance so your team arrives to a clean space.',
        define='Commercial cleaning is a scheduled service that cleans offices, reception areas, kitchenettes and bathrooms in a workspace, timed to the business’s access hours so staff and visitors arrive to a clean space.',
        fit_yes=['Offices, reception areas and shared workspaces near Natick.', 'You need cleaning timed around when the space is in use.', 'You want one direct contact for scope and scheduling.'],
        fit_no=['Specialized industrial cleaning: ask first, as it may be outside the scope offered.', 'A home office inside your house is covered by <a class="inline-link" href="/regular-cleaning.html">regular house cleaning</a>.'],
        focus_title='Your workspace. Your priorities.',
        focus_text='A commercial space needs a cleaning plan that reflects how it is used. Share the layout, shared areas and access requirements, and we confirm the service that fits your request.',
        focus=[('Office and shared workspace priorities', 'Desks and work areas, as agreed in the scope.'), ('Reception and common areas', 'The first impression for visitors.'), ('Kitchenette and bathroom needs', 'The shared rooms that need regular care.'), ('Access instructions and preferred timing', 'Keys, alarm codes and hours agreed beforehand.')],
        factors=[('Size and layout', 'Square footage, rooms and shared areas set the base time.'), ('How the space is used', 'Staff count and visitor traffic change the work.'), ('Kitchens and restrooms', 'The number of shared rooms affects each visit.'), ('Frequency', 'Recurring schedules are planned around your week.'), ('Access hours', 'Cleaning times are confirmed with availability before booking.')],
        related=f'Commercial cleaning is for workspaces used by a team and their visitors. For a home, including a home office, <a class="inline-link" href="/regular-cleaning.html">residential cleaning on a routine</a> is the better fit, and a property changing tenants is covered by <a class="inline-link" href="/move-in-move-out-cleaning.html">cleaning between occupants</a>. To check whether your business address is within reach, see <a class="inline-link" href="/service-areas.html">towns within 25 miles of Natick</a>.',
        faqs=[
            ('Can cleaning be arranged around business hours?', 'Share your preferred times when you request a quote. Scheduling and access arrangements are confirmed before booking, based on availability. Cleaning outside your busiest hours is often easiest for staff and visitors, so tell us when the space is open, when it is quiet and how access will be provided.'),
            ('What kinds of workspaces do you clean?', 'Neat Cleaning provides commercial cleaning for local workspaces in the Natick area, covering offices and shared work areas, reception and common areas, and the kitchenettes and bathrooms used by staff. Tell us the type of property and how it is used, and we confirm whether the request fits the commercial cleaning offered.'),
            ('Do you provide specialized industrial cleaning?', 'Contact us with the exact type of property and cleaning required. Neat Cleaning’s commercial service is designed for everyday workspaces. Specialized industrial cleaning may fall outside that scope, and we will tell you clearly whether your request is something we can take on before any quote is given.'),
            ('How is commercial cleaning priced?', 'Each workspace is quoted individually. The size of the space, how it is used, the number of bathrooms and kitchen areas, how often you need cleaning and the access hours all affect the price. Share those details and you receive a quote confirmed before booking. Payment is accepted by Zelle, cash or check.'),
            ('Can you clean on a recurring schedule?', 'Recurring commercial cleaning can be discussed when you request your quote. Tell us the frequency you have in mind, such as weekly or every other week, and your preferred days and times. The schedule is confirmed based on availability before booking, so your team knows when to expect each visit.'),
            ('Do you bring cleaning products?', 'Yes, Neat Cleaning brings its own cleaning products. If your business requires specific products, for example for certain surfaces or for staff with sensitivities, tell us when you request your quote. Special product requests are discussed in advance and may affect the quote.'),
        ]),
}



LEGAL_PRIVACY = [
    ('Information you provide', 'When you request a quote, we collect your name, phone number, email address, chosen service, town or ZIP code, any details you submit, and your consent to contact. Avoid sending sensitive personal information in the details field.'),
    ('How the information is used', 'We use your information to respond to your request, discuss a cleaning quote, coordinate appointments and provide customer care. Quote requests are emailed to Neat Cleaning’s designated mailbox.'),
    ('Calls, text messages and consent', 'Submitting the form requires explicit consent to calls and text messages about your request. Consent is not a condition of purchase. Message frequency varies, and message and data rates may apply. Reply STOP to opt out or HELP for help. You may also contact us by phone or email to discuss communication preferences.</p><p>This form does not request marketing consent. Any future promotional text program would require a separate opt-in. Mobile phone numbers and SMS opt-in data or consent will not be sold or shared with third parties or affiliates for their marketing or promotional purposes.'),
    ('Consent records and protection', 'The email generated by your submission includes the consent wording, the consent status, the form source and the submission time. Neat Cleaning uses these records to document the request and consent. Access should be limited to people handling customer communications.'),
    ('Service providers and disclosures', 'Website hosting and email providers process information as needed to operate the website and deliver requests. Information may also be disclosed when required by applicable law. SMS opt-in data and consent are excluded from sharing for third-party marketing.'),
    ('Technical information', 'The form endpoint temporarily uses an IP-derived identifier and a short submission interval to help prevent abuse. Hosting providers may maintain server access logs. The website does not include advertising trackers or analytics scripts. Fonts are served from this website, so no font requests are sent to third parties.'),
    ('Retention and your choices', 'We retain inquiry and consent information as needed to handle the request, maintain customer records and satisfy applicable obligations. Contact us to request access, correction or deletion of your information, subject to applicable retention requirements.'),
    ('Security', 'The form validates submissions and restricts the recipient on the server. No internet transmission or email storage can be guaranteed completely secure. Use the published HTTPS website when submitting personal information.'),
    ('Contact', f'For privacy or consent questions, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="{TEL}">{PHONE}</a>.'),
]
LEGAL_TERMS = [
    ('Website and quote requests', 'This website provides information about Neat Cleaning and lets you request a cleaning quote. Submitting the form is an inquiry, not a confirmed appointment or a payment transaction.'),
    ('Scope, pricing and appointments', 'Availability, the final cleaning scope, pricing, access instructions and timing are discussed directly before an appointment is confirmed. Special product requests or property requirements may affect the quote. Oven and refrigerator cleaning are included without a separate extra charge; discuss access and preparation when requesting your quote.'),
    ('Offer', 'A 10% OFF offer is available to discuss with Neat Cleaning. Mention it when you request your quote. Its application to your booking is confirmed directly before you agree to the service.'),
    ('Payments and changes', 'Payment methods are Zelle, cash and check. Contact Neat Cleaning directly to discuss payment arrangements, scheduling changes or questions about the service.'),
    ('SMS Terms', f'Program name: Neat Cleaning Customer Care Text Messages.</p><p>Description: By opting in, you may receive customer care messages about your cleaning quote, appointment coordination, confirmations, reminders and service questions. This website form does not enroll you in promotional marketing messages.</p><p>Message frequency varies. Message and data rates may apply. Consent is not a condition of purchase. You may contact us by phone or email if you prefer another way to make an inquiry.</p><p>To stop receiving text messages, reply STOP at any time. You may receive one final message confirming that you have been unsubscribed. For help, reply HELP or contact <a href="mailto:{EMAIL}">{EMAIL}</a> or <a href="{TEL}">{PHONE}</a>. Carriers are not liable for delayed or undelivered messages.</p><p>Mobile numbers, SMS opt-in data and consent are not sold or shared with third parties or affiliates for marketing or promotional purposes. See the <a href="/privacy-policy.html">Privacy Policy</a> for information about how inquiry and consent data are handled.'),
    ('Website imagery and content', 'The website uses generated illustrative images of homes and workspaces. They are not photographs of completed Neat Cleaning projects, customer properties or team members. Service information should be confirmed directly if you have a specific request.'),
    ('Contact', f'For questions about these terms, contact Neat Cleaning at <a href="mailto:{EMAIL}">{EMAIL}</a> or <a href="{TEL}">{PHONE}</a>.'),
]


