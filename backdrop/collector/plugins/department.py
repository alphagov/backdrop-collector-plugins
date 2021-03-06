import re


class ComputeDepartmentKey(object):

    """
    Adds a 'department' key to a dictionary by looking up the department from
    the specified, key_name. It takes the first department code of form
    <[code]> from document[key_name].
    """

    def __init__(self, key_name):
        self.key_name = key_name

    def __call__(self, documents):
        def compute_department(department):
            assert self.key_name in document, (
                'key "{}" not found "{}"'.format(self.key_name, document))
            department_codes = document[self.key_name]
            department_code = take_first_department_code(department_codes)
            document["department"] = DEPARTMENT_MAPPING.get(
                department_code, department_code)
            return document

        return [compute_department(document) for document in documents]


class SetDepartment(object):

    """
    Adds a 'department' key to a dictionary by using the department specified
    in the constructor. It takes the first department code of form <[code]>,
    and if that doesn't exist it uses the string verbatim.

    This assumes that all of the data being processed belongs to the same
    single department.

    For example:

        SetDepartment("<D3>")
        SetDepartment("Department for fooing the bar")
    """

    def __init__(self, department_or_code):
        self.department_or_code = department_or_code
        self.value = try_get_department(self.department_or_code)

    def __call__(self, documents):
        for document in documents:
            document["department"] = self.value
        return documents


def try_get_department(department_or_code):
    """
    Try to take the first department code, or fall back to string as passed
    """
    try:
        value = take_first_department_code(department_or_code)
    except AssertionError:
        value = department_or_code

    if value in DEPARTMENT_MAPPING:
        value = DEPARTMENT_MAPPING[value]

    return value


def test_try_get_department():
    from nose.tools import assert_equal
    assert_equal(try_get_department("<D1>"), "attorney-generals-office")
    assert_equal(try_get_department("<D1><foo>"), "attorney-generals-office")
    assert_equal(try_get_department("<foo>"), "<foo>")


def take_first_department_code(department_codes):
    get_first_re = re.compile("^(<[^>]+>).*$")
    match = get_first_re.match(department_codes)
    assert match is not None
    (department_code, ) = match.groups()
    return department_code


def test_mapping():
    from nose.tools import assert_equal, assert_in

    plugin = ComputeDepartmentKey("key_name")
    documents = [{"key_name": "<D10>"}]
    (transformed_document, ) = plugin(documents)

    assert_in("department", transformed_document)
    assert_equal(transformed_document["department"],
                 "department-for-work-pensions")


def test_fail_if_no_key_name_in_document():
    from nose.tools import assert_raises

    plugin = ComputeDepartmentKey("key_name")
    documents = [{"foo": "<D10>"}]

    with assert_raises(AssertionError):
        plugin(documents)


def test_unknown_department_code():
    from nose.tools import assert_equal

    plugin = ComputeDepartmentKey("key_name")
    documents = [{"key_name": "<DTHISDOESNOTEXIST>"}]
    (transformed_document, ) = plugin(documents)

    assert_equal(transformed_document["department"], "<DTHISDOESNOTEXIST>")


def test_takes_first_code():
    from nose.tools import assert_equal

    plugin = ComputeDepartmentKey("key_name")
    documents = [{"key_name": "<D10><D9>"}]
    (transformed_document, ) = plugin(documents)

    assert_equal(transformed_document["department"],
                 "department-for-work-pensions")


DEPARTMENT_MAPPING = {
    "<D1>": "attorney-generals-office",
    "<D2>": "cabinet-office",
    "<D3>": "department-for-business-innovation-skills",
    "<D4>": "department-for-communities-and-local-government",
    "<D5>": "department-for-culture-media-sport",
    "<D6>": "department-for-education",
    "<D7>": "department-for-environment-food-rural-affairs",
    "<D8>": "department-for-international-development",
    "<D9>": "department-for-transport",
    "<D10>": "department-for-work-pensions",
    "<D11>": "department-of-energy-climate-change",
    "<D12>": "department-of-health",
    "<D13>": "foreign-commonwealth-office",
    "<D15>": "hm-treasury",
    "<D16>": "home-office",
    "<D17>": "ministry-of-defence",
    "<D18>": "ministry-of-justice",
    "<D19>": "northern-ireland-office",
    "<D20>": "office-of-the-advocate-general-for-scotland",
    "<D21>": "the-office-of-the-leader-of-the-house-of-commons",
    "<D22>": "office-of-the-leader-of-the-house-of-lords",
    "<D23>": "scotland-office",
    "<D24>": "wales-office",
    "<D25>": "hm-revenue-customs",
    "<D30>": "treasury-solicitor-s-department",
    "<D38>": "ordnance-survey",
    "<D85>": "forestry-commission",
    "<D98>": "the-charity-commission-for-england-and-wales",
    "<D101>": "crown-prosecution-service",
    "<D102>": "food-standards-agency",
    "<D106>": "ofsted",
    "<D108>": "ofgem",
    "<D109>": "office-of-qualifications-and-examinations-regulation",
    "<D110>": "office-of-rail-regulation",
    "<D115>": "serious-fraud-office",
    "<D116>": "uk-statistics-authority",
    "<D117>": "uk-trade-investment",
    "<D240>": "the-water-services-regulation-authority",
    "<D241>": "uk-export-finance",
    "<D303>": "office-for-national-statistics",
    "<D346>": "public-works-loan-board",
    "<D352>": "office-of-fair-trading",
    "<D435>": "supreme-court-of-the-united-kingdom",
    "<EA26>": "companies-house",
    "<EA31>": "uk-space-agency",
    "<EA32>": "insolvency-service",
    "<EA33>": "national-measurement-office",
    "<EA34>": "intellectual-property-office",
    "<EA37>": "fire-service-college",
    "<EA39>": "planning-inspectorate",
    "<EA40>": "queen-elizabeth-ii-conference-centre",
    "<EA41>": "royal-parks",
    "<EA42>": "defence-science-and-technology-laboratory",
    "<EA44>": "defence-support-group",
    "<EA46>": "met-office",
    "<EA47>": "ministry-of-defence-police-and-guarding-agency",
    "<EA49>": "service-children-s-education",
    "<EA50>": "service-personnel-and-veterans-agency",
    "<EA51>": "uk-hydrographic-office",
    "<EA52>": "animal-health-and-veterinary-laboratories-agency",
    "<EA53>": "centre-for-environment-fisheries-and-aquaculture-science",
    "<EA54>": "forest-research",
    "<EA55>": "forest-enterprise-england",
    "<EA56>": "the-food-and-environment-research-agency",
    "<EA58>": "rural-payments-agency",
    "<EA60>": "veterinary-medicines-directorate",
    "<EA61>": "fco-services",
    "<EA62>": "wilton-park",
    "<EA63>": "medicines-and-healthcare-products-regulatory-agency",
    "<EA66>": "identity-and-passport-service",
    "<EA67>": "uk-border-agency",
    "<EA70>": "national-offender-management-service",
    "<EA71>": "the-national-archives",
    "<EA72>": "office-of-the-public-guardian",
    "<EA73>": "hm-courts-and-tribunals-service",
    "<EA74>": "driver-and-vehicle-licensing-agency",
    "<EA75>": "driving-standards-agency",
    "<EA77>": "highways-agency",
    "<EA78>": "maritime-and-coastguard-agency",
    "<EA79>": "vehicle-and-operator-services-agency",
    "<EA80>": "vehicle-certification-agency",
    "<EA82>": "uk-debt-management-office",
    "<EA86>": "skills-funding-agency",
    "<EA87>": "valuation-office-agency",
    "<EA104>": "ns-i",
    "<EA114>": "royal-mint",
    "<EA199>": "environment-agency",
    "<EA242>": "education-funding-agency",
    "<EA243>": "standards-and-testing-agency",
    "<EA245>": "national-college-for-school-leadership",
    "<EA321>": "hm-prison-service",
    "<EA365>": "government-procurement-service",
    "<EA480>": "public-health-england",
    "<EA541>": "national-college-for-teaching-and-leadership",
    "<EA570>": "driver-and-vehicle-standards-agency",
    "<IM320>": "criminal-cases-review-commission",
    "<IM324>": "hm-inspectorate-of-prisons",
    "<IM325>": "hm-inspectorate-of-probation",
    "<IM327>": "prisons-and-probation-ombudsman",
    "<IM329>": "the-legal-ombudsman",
    "<IM332>": "legal-services-board",
    "<IM333>": "judicial-appointments-and-conduct-ombudsman",
    "<IM335>": "independent-commission-for-aid-impact",
    "<IM341>": "house-of-lords-appointments-commission",
    "<OT100>": "the-crown-estate",
    "<OT152>": "industrial-development-advisory-board",
    "<OT204>": "agriculture-and-horticulture-development-board",
    "<OT205>": "sea-fish-industry-authority",
    "<OT214>": "covent-garden-market-authority",
    "<OT216>": "broads-authority",
    "<OT217>": "dartmoor-national-park-authority",
    "<OT219>": "exmoor-national-park-authority",
    "<OT220>": "lake-district-national-park-authority",
    "<OT222>": "new-forest-national-park-authority",
    "<OT223>": "north-york-moors-national-park",
    "<OT237>": "national-employment-savings-trust",
    "<OT248>": "air-accidents-investigation-branch",
    "<OT249>": "rail-accidents-investigation-branch",
    "<OT261>": "office-of-tax-simplification",
    "<OT269>": "equality-and-human-rights-commission",
    "<OT281>": "hm-inspectorate-of-constabulary",
    "<OT284>": "chief-inspector-of-the-uk-border-agency",
    "<OT304>": "the-security-service-mi5",
    "<OT305>": "secret-intelligence-service",
    "<OT306>": "government-communications-headquarters",
    "<OT313>": "british-council",
    "<OT315>": "marshall-aid-commemoration-commission",
    "<OT316>": "westminster-foundation-for-democracy",
    "<OT328>": "official-solicitor-and-public-trustee",
    "<OT342>": "privy-council-office",
    "<OT347>": "hm-crown-prosecution-service-inspectorate",
    "<OT360>": "uk-green-investment-bank",
    "<OT385>": "ofcom",
    "<OT404>": "service-complaints-commissioner",
    "<OT405>": "defence-academy",
    "<OT406>": "service-prosecuting-authority",
    "<OT408>": "defence-press-and-broadcasting-advisory-committee",
    "<OT409>": "royal-navy-submarine-museum",
    "<OT411>": "defence-sixth-form-college",
    "<OT425>": "drinking-water-inspectorate",
    "<OT428>": "boundary-commission-for-northern-ireland",
    "<OT429>": "northern-ireland-human-rights-commission",
    "<OT430>": "parades-commission-for-northern-ireland",
    "<OT431>": "boundary-commission-for-scotland",
    "<OT432>": "boundary-commission-for-wales",
    "<OT433>": "the-adjudicator-s-office",
    "<OT444>": "independent-monitoring-boards-of-prisons-immigration-removal-"
               "centres-and-short-term-holding-rooms",
    "<OT483>": "health-research-authority",
    "<OT484>": "nhs-trust-development-authority",
    "<OT486>": "nhs-blood-and-transplant",
    "<OT488>": "nhs-litigation-authority",
    "<OT492>": "chevening-foundation",
    "<OT494>": "airports-commission",
    "<OT495>": "defence-equipment-and-support",
    "<OT496>": "defence-infrastructure-organisation",
    "<OT498>": "joint-forces-command",
    "<OT502>": "office-for-life-sciences",
    "<OT504>": "chief-fire-and-rescue-adviser-unit",
    "<OT505>": "national-security",
    "<OT506>": "government-equalities-office",
    "<OT507>": "efficiency-and-reform-group",
    "<OT511>": "independent-reviewer-of-terrorism-legislation",
    "<OT512>": "intelligence-services-commissioner",
    "<OT513>": "interception-of-communications-commissioner",
    "<OT514>": "office-for-low-emission-vehicles",
    "<OT515>": "office-of-the-parliamentary-counsel",
    "<OT517>": "commissioner-for-public-appointments",
    "<OT518>": "mckay-commission",
    "<OT519>": "the-parliamentary-and-health-service-ombudsman",
    "<OT520>": "behavioural-insights-team",
    "<OT522>": "advisory-committee-on-clinical-excellence-awards",
    "<OT529>": "nhs-business-services-authority",
    "<OT532>": "prime-ministers-office-10-downing-street",
    "<OT533>": "investigation-into-the-role-of-jimmy-savile-at-broadmoor-"
               "hospital",
    "<OT535>": "border-force",
    "<OT536>": "forensic-science-regulator",
    "<OT537>": "deputy-prime-ministers-office",
    "<OT538>": "health-and-social-care-information-centre",
    "<OT539>": "health-education-england",
    "<OT540>": "infrastructure-uk",
    "<OT554>": "uk-visas-and-immigration",
    "<PB27>": "student-loans-company",
    "<PB28>": "acas",
    "<PB29>": "national-fraud-authority",
    "<PB57>": "marine-management-organisation",
    "<PB118>": "horserace-betting-levy-board",
    "<PB120>": "higher-education-funding-council-for-england",
    "<PB121>": "council-for-science-and-technology",
    "<PB122>": "low-pay-commission",
    "<PB123>": "arts-and-humanities-research-council",
    "<PB124>": "british-hallmarking-council",
    "<PB126>": "construction-industry-training-board",
    "<PB129>": "economic-and-social-research-council",
    "<PB130>": "engineering-and-physical-sciences-research-council",
    "<PB131>": "engineering-construction-industry-training-board",
    "<PB132>": "medical-research-council",
    "<PB133>": "natural-environment-research-council",
    "<PB134>": "office-for-fair-access",
    "<PB135>": "science-and-technology-facilities-council",
    "<PB136>": "technology-strategy-board",
    "<PB137>": "uk-atomic-energy-authority",
    "<PB138>": "uk-commission-for-employment-and-skills",
    "<PB139>": "certification-office",
    "<PB140>": "competition-appeal-tribunal",
    "<PB147>": "capital-for-enterprise-ltd",
    "<PB148>": "central-arbitration-committee",
    "<PB158>": "the-committee-on-standards-in-public-life",
    "<PB160>": "building-regulations-advisory-committee",
    "<PB161>": "homes-and-communities-agency",
    "<PB165>": "arts-council-england",
    "<PB166>": "british-library",
    "<PB167>": "british-museum",
    "<PB168>": "english-heritage",
    "<PB169>": "gambling-commission",
    "<PB170>": "geffrye-museum",
    "<PB171>": "horniman-museum",
    "<PB172>": "imperial-war-museum",
    "<PB174>": "national-gallery",
    "<PB175>": "national-heritage-memorial-fund",
    "<PB176>": "national-lottery-commission",
    "<PB177>": "science-museum-group",
    "<PB178>": "national-museums-liverpool",
    "<PB179>": "national-portrait-gallery",
    "<PB180>": "natural-history-museum",
    "<PB181>": "olympic-delivery-authority",
    "<PB182>": "royal-armouries-museum",
    "<PB183>": "sir-john-soane-s-museum",
    "<PB184>": "sports-grounds-safety-authority",
    "<PB185>": "uk-sport",
    "<PB186>": "visitbritain",
    "<PB187>": "wallace-collection",
    "<PB188>": "big-lottery-fund",
    "<PB189>": "british-film-institute",
    "<PB190>": "sport-england",
    "<PB191>": "committee-on-radioactive-waste-management",
    "<PB192>": "the-fuel-poverty-advisory-group",
    "<PB193>": "nuclear-liabilities-financing-assurance-board",
    "<PB194>": "civil-nuclear-police-authority",
    "<PB195>": "the-coal-authority",
    "<PB196>": "committee-on-climate-change",
    "<PB197>": "nuclear-decommissioning-authority",
    "<PB198>": "consumer-council-for-water",
    "<PB200>": "gangmasters-licensing-authority",
    "<PB201>": "joint-nature-conservation-committee",
    "<PB202>": "natural-england",
    "<PB207>": "health-and-safety-executive",
    "<PB208>": "advisory-committee-on-pesticides",
    "<PB209>": "advisory-committee-on-releases-to-the-environment",
    "<PB210>": "independent-agricultural-appeals-panel",
    "<PB211>": "science-advisory-council",
    "<PB212>": "veterinary-products-committee",
    "<PB213>": "agricultural-land-tribunal",
    "<PB226>": "commonwealth-scholarship-commission-in-the-uk",
    "<PB230>": "equality-2025",
    "<PB231>": "industrial-injuries-advisory-council",
    "<PB232>": "social-security-advisory-committee",
    "<PB233>": "the-pensions-advisory-service",
    "<PB234>": "the-pensions-regulator",
    "<PB235>": "pension-protection-fund-ombudsman",
    "<PB236>": "pensions-ombudsman",
    "<PB246>": "children-and-family-court-advisory-and-support-service",
    "<PB247>": "disabled-persons-transport-advisory-committee",
    "<PB251>": "care-quality-commission",
    "<PB253>": "human-fertilisation-and-embryology-authority",
    "<PB254>": "human-tissue-authority",
    "<PB255>": "monitor",
    "<PB257>": "foreign-compensation-commission",
    "<PB260>": "office-for-budget-responsibility",
    "<PB263>": "office-of-the-immigration-services-commissioner",
    "<PB264>": "security-industry-authority",
    "<PB265>": "serious-organised-crime-agency",
    "<PB266>": "office-of-manpower-economics",
    "<PB270>": "investigatory-powers-tribunal",
    "<PB271>": "advisory-council-on-the-misuse-of-drugs",
    "<PB273>": "police-advisory-board-for-england-and-wales",
    "<PB274>": "technical-advisory-board",
    "<PB275>": "migration-advisory-committee",
    "<PB276>": "national-dna-database-ethics-group",
    "<PB277>": "police-arbitration-tribunal",
    "<PB278>": "police-discipline-appeals-tribunal",
    "<PB290>": "royal-naval-museum",
    "<PB291>": "royal-museums-greenwich",
    "<PB293>": "civil-justice-council",
    "<PB294>": "law-commission",
    "<PB295>": "the-sentencing-council-for-england-and-wales",
    "<PB296>": "victim-s-advisory-panel",
    "<PB297>": "criminal-injuries-compensation-authority",
    "<PB298>": "information-commissioner-s-office",
    "<PB299>": "judicial-appointments-commission",
    "<PB300>": "legal-services-commission",
    "<PB301>": "parole-board",
    "<PB302>": "youth-justice-board-for-england-and-wales",
    "<PB307>": "national-army-museum",
    "<PB308>": "royal-air-force-museum",
    "<PB310>": "royal-marines-museum",
    "<PB311>": "fleet-air-arm-museum",
    "<PB317>": "biotechnology-biological-sciences-research-council",
    "<PB318>": "competition-service",
    "<PB326>": "victims-commissioner",
    "<PB336>": "advisory-committee-on-business-appointments",
    "<PB337>": "boundary-commission-for-england",
    "<PB348>": "pension-protection-fund",
    "<PB349>": "independent-living-fund",
    "<PB350>": "remploy-ltd",
    "<PB353>": "competition-commission",
    "<PB354>": "regulatory-policy-committee",
    "<PB355>": "copyright-tribunal",
    "<PB356>": "consumer-focus",
    "<PB357>": "export-guarantees-advisory-council",
    "<PB358>": "land-registration-rule-committee",
    "<PB366>": "civil-service-commission",
    "<PB367>": "security-vetting-appeals-panel",
    "<PB368>": "review-body-on-senior-salaries",
    "<PB372>": "housing-ombudsman",
    "<PB373>": "leasehold-advisory-service",
    "<PB374>": "london-thames-gateway-development-corporation",
    "<PB375>": "valuation-tribunal-service-for-england-valuation-tribunal-"
               "service",
    "<PB376>": "visitengland",
    "<PB377>": "uk-anti-doping",
    "<PB378>": "victoria-and-albert-museum",
    "<PB380>": "the-theatres-trust",
    "<PB381>": "olympic-lottery-distributor",
    "<PB382>": "the-reviewing-committee-on-the-export-of-works-of-art-and-"
               "objects-of-cultural-interest",
    "<PB383>": "treasure-valuation-committee",
    "<PB392>": "advisory-committee-on-conscientious-objectors",
    "<PB393>": "advisory-group-on-military-medicine",
    "<PB394>": "armed-forces-pay-review-body",
    "<PB395>": "central-advisory-committee-on-pensions-and-compensation",
    "<PB396>": "defence-nuclear-safety-committee",
    "<PB397>": "defence-scientific-advisory-council",
    "<PB399>": "national-employer-advisory-board",
    "<PB400>": "nuclear-research-advisory-council",
    "<PB401>": "oil-and-pipelines-agency",
    "<PB402>": "science-advisory-committee-on-the-medical-implications-of-"
               "less-lethal-weapons",
    "<PB403>": "veterans-advisory-and-pensions-committees-x13",
    "<PB413>": "office-of-the-children-s-commissioner",
    "<PB414>": "school-teachers-review-body",
    "<PB415>": "national-forest-company",
    "<PB420>": "agricultural-wages-committee-x13",
    "<PB421>": "agricultural-dwelling-house-advisory-committees-x16",
    "<PB423>": "plant-varieties-and-seeds-tribunal",
    "<PB426>": "great-britain-china-centre",
    "<PB434>": "royal-mint-advisory-committee",
    "<PB436>": "administrative-justice-and-tribunals-council",
    "<PB437>": "advisory-committees-on-justices-of-the-peace",
    "<PB438>": "the-advisory-council-on-national-records-and-archives",
    "<PB440>": "civil-procedure-rules-committee",
    "<PB441>": "family-justice-council",
    "<PB442>": "family-procedure-rule-committee",
    "<PB443>": "independent-advisory-panel-on-deaths-in-custody",
    "<PB445>": "insolvency-rules-committee",
    "<PB446>": "prison-services-pay-review-body",
    "<PB448>": "tribunal-procedure-committee",
    "<PB456>": "independent-police-complaint-commission",
    "<PB457>": "office-of-surveillance-commissioners",
    "<PB458>": "police-negotiating-board",
    "<PB459>": "directly-operated-railways-limited",
    "<PB460>": "high-speed-two-limited",
    "<PB461>": "british-transport-police-authority",
    "<PB462>": "trinity-house",
    "<PB463>": "northern-lighthouse-board",
    "<PB464>": "passenger-focus",
    "<PB465>": "traffic-commissioners",
    "<PB466>": "railway-heritage-committee",
    "<PB474>": "national-institute-for-clinical-excellence",
    "<PB477>": "review-board-for-government-contracts",
    "<PB481>": "nhs-commissioning-board",
    "<PB491>": "advisory-panel-on-public-sector-information",
    "<PB500>": "the-shareholder-executive",
    "<PB501>": "the-west-northamptonshire-development-corporation",
    "<PB503>": "local-government-ombudsman",
    "<PB508>": "board-of-trustees-of-the-royal-botanic-gardens-kew",
    "<PB509>": "disclosure-and-barring-service",
    "<PB510>": "social-mobility-and-child-poverty-commission",
    "<PB516>": "criminal-procedure-rule-committee",
    "<PB521>": "insolvency-practitioners-tribunal",
    "<PB523>": "administration-of-radioactive-substances-advisory-committee",
    "<PB524>": "british-pharmacopoeia",
    "<PB525>": "commission-on-human-medicines",
    "<PB526>": "committee-on-mutagenicity-of-chemicals-in-food-consumer-"
               "products-and-the-environment",
    "<PB527>": "independent-reconfiguration-panel",
    "<PB530>": "review-body-on-doctors-and-dentists-remuneration",
    "<PB531>": "nhs-pay-review-body",
    "<PB534>": "animals-in-science-committee",
    "<PB542>": "the-office-of-the-schools-commissioner",
    "<PC163>": "architects-registration-board",
    "<PC259>": "uk-financial-investments-limited",
    "<PC343>": "audit-commission",
    "<PC386>": "channel-4",
    "<PC387>": "s4c",
    "<PC388>": "bbc",
    "<PC389>": "historic-royal-palaces",
    "<PC390>": "heritage-lottery-fund",
    "<PC427>": "bbc-world-service",
    "<PC467>": "brb-residuary-ltd",
    "<PC468>": "trust-ports",
    "<PC469>": "civil-aviation-authority",
    "<PC472>": "marine-accident-investigation-branch",
    "<PC493>": "london-and-continental-railways-ltd",
}
