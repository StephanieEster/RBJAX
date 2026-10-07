"""Business data and site copy for Rio Cleaning Services LLC.

Everything a non-developer may need to change lives here. After editing, run
`python3 build/build.py` from the rio-cleaning folder to regenerate site/.

Claims policy: only facts confirmed in the client briefing are published. Do not add
review counts, star ratings, guarantees, "bonded", "background checked", prices or
city names unless the business has confirmed them in writing.
"""

# ------------------------------------------------------------------ business
SITE_URL = 'https://riocleanings.com'          # final domain, no trailing slash
NAME = 'Rio Cleaning Services'
LEGAL_NAME = 'Rio Cleaning Services LLC'
PHONE = '(267) 694-4609'
PHONE_E164 = '+12676944609'
TEL = 'tel:+12676944609'
EMAIL = 'riocleaningservices.m@gmail.com'
BASE_CITY = 'Philadelphia'
BASE_REGION = 'PA'
FOUNDED = '2019'
OWNER = 'Marcia'

# Office hours as published on the previous website. VERIFY against the Google
# Business Profile before launch; set to None to hide them everywhere.
HOURS = {'label': 'Monday–Friday, 7 AM – 5 PM', 'short': 'Mon–Fri, 7 AM – 5 PM',
         'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '07:00', 'closes': '17:00'}

INSTAGRAM = 'https://www.instagram.com/riocleaningservices_'
FACEBOOK = 'https://www.facebook.com/riodejaneirocleaningservices'   # linked from the previous official site
GOOGLE_PROFILE = ''   # paste the official Google Business Profile link once confirmed

PAYMENTS = ['Zelle', 'Venmo', 'Credit card', 'Check', 'Cash']

# Real, verifiable reviews only (from Google or the client). Each item:
# {'name': 'First name + last initial', 'text': '...', 'source': 'Google', 'url': 'https://...'}
REVIEWS = []

# Cities confirmed by the business. Each confirmed city can get its own page later
# (see LEIA-ME.md). Leave empty until the business sends the list.
CONFIRMED_CITIES = []

# One authorized promotion at a time, or None. Example:
# OFFER = {'title': 'Refer a friend, get $50', 'text': '...', 'terms': '...'}
OFFER = None

# The estimate form posts to /send.php (PHP on Hostinger). Delivery settings
# (recipient, SMTP mailbox, backups) live in site/includes/config.php.
FORM_ACTION = '/send.php'

# Tracking IDs. Leave empty until the real IDs exist; nothing is loaded while empty.
TRACKING = {
    'gtm': '',            # e.g. GTM-XXXXXXX
    'ga4': '',            # e.g. G-XXXXXXXXXX (skip if GA4 is configured inside GTM)
    'google_ads': '',     # e.g. AW-XXXXXXXXX
    'google_ads_form_label': '',   # conversion label for quote_form_submit
    'google_ads_call_label': '',   # conversion label for phone_click
    'meta_pixel': '',     # e.g. 1234567890
}

UPDATED = 'October 2026'
UPDATED_ISO = '2026-10-07'

# ------------------------------------------------------------------ shared facts
TRUST = [
    ('award', 'Nearly 25 years', 'of hands-on cleaning experience'),
    ('shield', 'Insured', 'for your peace of mind'),
    ('home', 'Locally owned', 'and operated in Philadelphia'),
    ('calendar', 'Flexible scheduling', 'designed around real life'),
]

DIFFERENTIATORS = [
    ('award', 'Experience you can see',
     'Our owner, Marcia, has nearly 25 years of hands-on residential cleaning experience. She knows the job '
     'because she has done it herself, in well over a thousand homes.'),
    ('repeat', 'Reliable, consistent visits',
     'Recurring clients get a routine they can count on. Several of our client relationships go back around '
     'eight years.'),
    ('eye', 'Attention to the small things',
     'Baseboards, handles, faucets and the corners most people notice only when they are dusty. The details '
     'are what make a home feel cared for.'),
    ('calendar', 'Flexibility when life happens',
     'With two teams, we can often rearrange a visit when your week changes. Just let us know as early as you can.'),
    ('message', 'You talk to the owner',
     'Marcia stays personally involved with clients, so questions and requests reach someone who can act on them.'),
    ('badge', 'We make it right',
     'If something doesn\'t meet expectations, let us know so we can make it right.'),
]

STEPS = [
    ('phone', 'Tell us about your home',
     'Call us or send a quick request with your home size, the service you need and how often.'),
    ('clipboard', 'Receive your estimate',
     'We learn about your home, its condition and your preferred frequency, then prepare a personalized estimate.'),
    ('calendar', 'Schedule your cleaning',
     'Choose an available day and time that works for your household.'),
    ('sparkles', 'Enjoy a cleaner home',
     'Our team handles the cleaning so you can focus on everything else.'),
]

ESTIMATE_NOTE = ('Every home is different. We\'ll confirm your cleaning plan and any add-ons when preparing '
                 'your estimate.')

ESTIMATE_FACTORS = [
    ('Size of your home', 'Bedrooms, bathrooms and overall square footage set the starting point.'),
    ('Type of cleaning', 'A recurring visit, a first-time deep clean, a move-in/move-out clean and carpet cleaning '
                         'each take a different amount of time.'),
    ('Current condition', 'Buildup, pet hair and how long it has been since the last professional cleaning.'),
    ('Frequency', 'Homes on a weekly or biweekly routine stay easier to maintain between visits.'),
    ('Special requests', 'Any add-ons or priority areas you want us to focus on.'),
]

# ------------------------------------------------------------------ what's included
INCLUDED = {
    'recurring': {
        'label': 'Recurring cleaning',
        'intro': 'Your regular weekly, biweekly or monthly visit keeps the whole house in good shape.',
        'groups': [
            ('utensils', 'Kitchen', ['Countertops and backsplash wiped', 'Sink and faucet cleaned',
                                     'Exterior of appliances wiped', 'Cabinet fronts and handles spot-cleaned']),
            ('bath', 'Bathrooms', ['Toilets, tubs and showers cleaned', 'Sinks, faucets and mirrors shined',
                                   'Counters wiped down']),
            ('sofa', 'Living areas & bedrooms', ['Reachable surfaces dusted', 'Floors vacuumed and mopped',
                                                 'Trash emptied']),
        ],
    },
    'deep': {
        'label': 'Deep / first-time cleaning',
        'intro': 'Everything in a recurring visit, with extra time for buildup and hard-to-reach areas.',
        'groups': [
            ('utensils', 'Kitchen', ['Detailed cleaning around fixtures and edges', 'Built-up grime on surfaces',
                                     'Cabinet fronts, handles and switches']),
            ('bath', 'Bathrooms', ['Soap scum and buildup on tubs, showers and tile', 'Fixtures and faucets detailed',
                                   'Around and behind the toilet base']),
            ('sofa', 'Throughout the home', ['Baseboards, door frames and trim', 'Hard-to-reach dust',
                                             'Floors cleaned edge to edge']),
        ],
    },
    'move': {
        'label': 'Move-in / move-out cleaning',
        'intro': 'A top-to-bottom clean of an empty home, so it is ready for the next chapter.',
        'groups': [
            ('utensils', 'Kitchen', ['Inside empty cabinets and drawers', 'Counters, sink and backsplash',
                                     'Exterior of appliances']),
            ('bath', 'Bathrooms', ['Toilets, tubs, showers and tile', 'Vanities, mirrors and fixtures',
                                   'Inside empty vanity cabinets']),
            ('door', 'Every room', ['Baseboards, trim and doors', 'Light switches and outlet covers',
                                    'Floors vacuumed and mopped']),
        ],
    },
}

# ------------------------------------------------------------------ FAQs
# key -> (question, answer). Answers use only facts confirmed by the business.
FAQ = {
    'cost': ('How much does house cleaning cost?',
             'Every home is different, so we don\'t publish one flat price. Your estimate depends on the size of your '
             'home, the type of cleaning, its current condition and how often you\'d like service. Call us at '
             f'{PHONE} or send a request, and we\'ll prepare a personalized estimate for your home at no cost.'),
    'regular-vs-deep': ('What\'s the difference between regular cleaning and deep cleaning?',
                        'A regular (recurring) cleaning maintains a home that is already in good shape: dusting, '
                        'kitchens, bathrooms, floors and trash. A deep cleaning takes more time and focuses on buildup '
                        'and the areas a routine visit doesn\'t reach every time, like baseboards, trim and soap scum. '
                        'Most new recurring clients start with a deep cleaning.'),
    'frequencies': ('Do you offer weekly and biweekly cleaning?',
                    'Yes. We offer weekly, biweekly and monthly house cleaning, as well as one-time visits. Biweekly '
                    'cleaning, every two weeks, is the schedule many families choose because it keeps the home '
                    'consistently clean without a visit every week. We\'ll help you pick the frequency that fits '
                    'your household.'),
    'which-frequency': ('Which cleaning frequency is right for my family?',
                        'Weekly works well for busy households with kids or pets where messes build up fast. Biweekly '
                        'suits most families in a 3-bedroom, 2–3 bathroom home: the house stays clean and your '
                        'weekends stay free. Monthly is a good fit for smaller or lightly used homes. You can always '
                        'adjust later.'),
    'areas': ('What areas do you serve?',
              'Rio Cleaning Services is based in Philadelphia and serves nearby communities in Pennsylvania, '
              'New Jersey and Delaware. Availability depends on your location and our teams\' schedules, so the '
              f'quickest way to confirm is to call {PHONE} or include your ZIP code in your estimate request.'),
    'insured': ('Are you insured?',
                'Yes. Rio Cleaning Services LLC is insured. If you need details for your building or homeowners '
                'association, ask us when you request your estimate.'),
    'experience': ('How long have you been in business?',
                   'Rio Cleaning Services LLC was established in 2019. It is backed by our owner Marcia\'s nearly '
                   '25 years of hands-on residential cleaning experience in the United States, during which she has '
                   'cleaned more than 1,000 homes and built client relationships that have lasted around eight years.'),
    'payment': ('What payment methods do you accept?',
                'We accept Zelle, Venmo, credit cards, checks and cash. We\'ll confirm how and when payment is '
                'handled when we schedule your cleaning.'),
    'reschedule': ('Can I reschedule my cleaning?',
                   'Yes, life happens. Let us know as early as you can and we\'ll work with you on a new time. Because '
                   'we run two teams, we can often rearrange a visit, though availability depends on the week.'),
    'home-during': ('Do I need to be home during the cleaning?',
                    'That\'s up to you. Some clients like to be home, others prefer to come back to a finished house. '
                    'Tell us what works for you and we\'ll agree on how we get in and any instructions before your '
                    'first visit.'),
    'prepare': ('How do I prepare for my first cleaning?',
                'Pick up clutter, toys and clothes so we can reach the surfaces, put away valuables and anything '
                'fragile you\'d rather we not handle, and let us know about pets and priority areas. If parking '
                'or entry needs instructions, share them ahead of time.'),
    'make-right': ('What if something wasn\'t cleaned the way I expected?',
                   'Tell us. If something doesn\'t meet expectations, let us know as soon as possible so we can '
                   'make it right. Clear feedback also helps us adjust your cleaning plan for future visits.'),
    'owner': ('Will I be able to talk to the owner?',
              'Yes. Our owner, Marcia, stays personally involved in client relationships. When you call, you are '
              'talking to a small local business, not a call center.'),
    'move-timing': ('When should I schedule a move-out or move-in cleaning?',
                    'Ideally after the furniture and boxes are out and before the new residents move in. An empty '
                    'home lets us reach inside cabinets, along baseboards and every corner of the floor. Call as soon '
                    'as you know your moving dates so we can find a time that fits.'),
    'carpet': ('Do you offer carpet cleaning?',
               'Yes. Carpet cleaning can be booked on its own or together with a deep cleaning or move-in/move-out '
               'cleaning. Tell us how many rooms, stairs or rugs you need cleaned and about any stains or pet areas, '
               'and we\'ll include it in your estimate.'),
    'carpet-prepare': ('How should I prepare for carpet cleaning?',
                       'Clear small items, toys and anything on the floor, and move light furniture if you can. Let us '
                       'know ahead of time about stains, pet areas or delicate rugs so we can plan the visit and '
                       'set expectations before we start.'),
    'first-deep': ('Do I need a deep cleaning before starting recurring service?',
                   'In most cases, yes. If your home hasn\'t been professionally cleaned recently, a first-time deep '
                   'cleaning gets it to a level that regular visits can maintain. We\'ll recommend what makes sense '
                   'for your home when we prepare your estimate.'),
    'estimate-how': ('How do I get an estimate?',
                     f'Call {PHONE} or fill out the estimate form on this site. Tell us the type of cleaning, how often '
                     'you\'d like service, the number of bedrooms and bathrooms and your ZIP code. We\'ll follow up to '
                     'confirm the details and prepare your estimate.'),
}

FAQ_GROUPS = [
    ('Pricing & estimates', ['cost', 'estimate-how', 'payment']),
    ('Services', ['regular-vs-deep', 'first-deep', 'frequencies', 'which-frequency', 'move-timing', 'carpet']),
    ('Scheduling & visits', ['reschedule', 'home-during', 'prepare', 'carpet-prepare']),
    ('About Rio Cleaning', ['experience', 'insured', 'owner', 'make-right', 'areas']),
]

# ------------------------------------------------------------------ service pages
SERVICES = [
    {
        'slug': 'recurring-cleaning',
        'name': 'Recurring House Cleaning',
        'short': 'Recurring Cleaning',
        'card_title': 'Recurring cleaning',
        'card_text': 'Weekly, biweekly or monthly visits that keep your home consistently clean. Biweekly is our '
                     'most-requested schedule for family homes.',
        'icon': 'repeat',
        'img': 'wiping-table',
        'img_alt': 'Cleaner in orange gloves wiping a marble coffee table in a bright living room',
        'title': 'Recurring House Cleaning: Weekly & Biweekly | Rio Cleaning',
        'desc': 'Weekly, biweekly and monthly house cleaning for Philadelphia-area homes. Flexible scheduling, '
                'an insured local team and nearly 25 years of experience.',
        'eyebrow': 'Weekly · Biweekly · Monthly',
        'h1': 'Recurring house cleaning in the Philadelphia area',
        'lede': 'A clean home that stays that way. Choose weekly, biweekly or monthly visits from a local, insured '
                'team, with flexible scheduling built around your household.',
        'definition': 'Recurring house cleaning is a scheduled weekly, biweekly or monthly service that maintains '
                      'kitchens, bathrooms, floors and living areas, so a family home stays consistently clean '
                      'between visits.',
        'service_type': 'Recurring house cleaning',
        'included': 'recurring',
        'for_who': [
            'Families and couples who want the house to stay clean, not just get clean once',
            'Homes of around 3 bedrooms and 2–3 bathrooms on a busy schedule',
            'Anyone tired of spending weekends catching up on cleaning',
        ],
        'not_for': ('If your home hasn\'t been professionally cleaned in a while, start with a ',
                    'deep-cleaning', 'first-time deep cleaning', ' and move to recurring visits after.'),
        'faqs': ['frequencies', 'which-frequency', 'first-deep', 'reschedule', 'home-during', 'cost'],
        'related': ['deep-cleaning', 'move-in-move-out-cleaning', 'carpet-cleaning'],
        'og': 'family-time',
    },
    {
        'slug': 'deep-cleaning',
        'name': 'Deep Cleaning',
        'short': 'Deep Cleaning',
        'card_title': 'Deep & first-time cleaning',
        'card_text': 'A detailed top-to-bottom clean for buildup and hard-to-reach areas. The right start before '
                     'recurring service.',
        'icon': 'sparkles',
        'img': 'bathroom-faucet',
        'img_alt': 'Gloved hand scrubbing a bathroom faucet with a sponge',
        'title': 'Deep Cleaning Services in Philadelphia, PA | Rio Cleaning',
        'desc': 'First-time and seasonal deep house cleaning for Philadelphia-area homes: buildup, baseboards, '
                'bathrooms and kitchens. Call for a free, personalized estimate.',
        'eyebrow': 'First-time · Seasonal · Catch-up',
        'h1': 'Deep cleaning services for Philadelphia-area homes',
        'lede': 'When your home needs more than a routine visit. A deep cleaning tackles buildup and the details '
                'that get skipped, and gives recurring service a clean starting point.',
        'definition': 'A deep cleaning is a detailed, top-to-bottom house cleaning that removes built-up grime, '
                      'soap scum and dust from areas a routine visit doesn\'t reach every time, usually booked as a '
                      'first-time or seasonal clean.',
        'service_type': 'Deep house cleaning',
        'included': 'deep',
        'for_who': [
            'Homes starting recurring service for the first time',
            'Seasonal resets, before hosting family or after a busy stretch',
            'Homes that haven\'t had a professional cleaning in a while',
        ],
        'not_for': ('If you\'re moving out or into an empty home, our ',
                    'move-in-move-out-cleaning', 'move-in and move-out cleaning', ' is built for that.'),
        'faqs': ['regular-vs-deep', 'first-deep', 'prepare', 'cost', 'home-during', 'make-right'],
        'related': ['recurring-cleaning', 'move-in-move-out-cleaning', 'carpet-cleaning'],
        'og': 'bathroom-faucet',
    },
    {
        'slug': 'move-in-move-out-cleaning',
        'name': 'Move-In & Move-Out Cleaning',
        'short': 'Move-In / Move-Out',
        'card_title': 'Move-in / move-out cleaning',
        'card_text': 'A thorough clean of an empty home, inside cabinets and along every baseboard, before the '
                     'keys change hands.',
        'icon': 'key',
        'img': 'moving-boxes',
        'img_alt': 'Cardboard moving boxes stacked in a bright, empty room',
        'title': 'Move-In & Move-Out Cleaning in Philadelphia | Rio Cleaning',
        'desc': 'Move-out and move-in cleaning for Philadelphia-area homes: inside cabinets, bathrooms, baseboards '
                'and floors in an empty house. Call for a free estimate.',
        'eyebrow': 'Moving out · Moving in',
        'h1': 'Move-in and move-out cleaning in the Philadelphia area',
        'lede': 'Moving is enough work. We clean the empty home, from inside the cabinets to the last baseboard, '
                'so you can hand over the keys or settle into a fresh start.',
        'definition': 'Move-in and move-out cleaning is a detailed cleaning of an empty home, including inside '
                      'cabinets and drawers, bathrooms, baseboards and floors, done between one resident leaving '
                      'and the next moving in.',
        'service_type': 'Move-in and move-out cleaning',
        'included': 'move',
        'for_who': [
            'Homeowners and renters leaving a home',
            'Families who want a clean house before unpacking',
            'Empty homes between residents',
        ],
        'not_for': ('If you\'re staying put and want regular help, take a look at ',
                    'recurring-cleaning', 'recurring house cleaning', ' instead.'),
        'faqs': ['move-timing', 'cost', 'carpet', 'payment', 'make-right', 'areas'],
        'related': ['deep-cleaning', 'carpet-cleaning', 'recurring-cleaning'],
        'og': 'moving-boxes',
    },
    {
        'slug': 'carpet-cleaning',
        'name': 'Carpet Cleaning',
        'short': 'Carpet Cleaning',
        'card_title': 'Carpet cleaning',
        'card_text': 'Carpets and rugs refreshed on their own, or paired with a deep or move-out clean.',
        'icon': 'carpet',
        'img': 'carpet-vacuum',
        'img_alt': 'Cordless cleaner running across a plush white rug next to a wooden bench',
        'title': 'Carpet Cleaning for Philadelphia-Area Homes | Rio Cleaning',
        'desc': 'Residential carpet cleaning for bedrooms, living rooms, stairs and rugs in the Philadelphia area. '
                'Book it alone or with a deep or move-out cleaning.',
        'eyebrow': 'Rooms · Stairs · Rugs',
        'h1': 'Carpet cleaning for Philadelphia-area homes',
        'lede': 'Carpets hold on to what floors let go: everyday dirt, pet hair and traffic lanes. Book carpet '
                'cleaning on its own or pair it with a deep or move-out cleaning.',
        'definition': 'Residential carpet cleaning refreshes wall-to-wall carpet, stairs and area rugs in a home, '
                      'focusing on embedded dirt, high-traffic areas and spots, and is often paired with a deep or '
                      'move-out cleaning.',
        'service_type': 'Residential carpet cleaning',
        'included': None,
        'for_who': [
            'High-traffic living rooms, hallways and stairs',
            'Homes with pets or young kids',
            'Move-outs, move-ins and seasonal deep cleans',
        ],
        'not_for': ('Need the rest of the house done too? Pair it with a ',
                    'deep-cleaning', 'deep house cleaning', ' in the same visit window.'),
        'faqs': ['carpet', 'carpet-prepare', 'cost', 'move-timing', 'payment', 'make-right'],
        'related': ['deep-cleaning', 'move-in-move-out-cleaning', 'recurring-cleaning'],
        'og': 'carpet-vacuum',
    },
]
SVC = {s['slug']: s for s in SERVICES}

FREQUENCIES = [
    ('Weekly', 'Busy households with kids, pets or a lot of daily traffic.',
     'The house rarely gets past "lived-in." Ideal if messes build up fast.'),
    ('Biweekly', 'Most family homes, especially 3 bedrooms and 2–3 bathrooms.',
     'Consistently clean, easy to keep up between visits, weekends stay free.'),
    ('Monthly', 'Smaller or lightly used homes, or a monthly reset.',
     'A thorough refresh once a month; more tidying in between.'),
    ('One-time', 'Special occasions, catch-up cleans or trying us out.',
     'A single visit. Many one-time clients move on to a recurring plan.'),
]
