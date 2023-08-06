import json, requests
from bs4 import BeautifulSoup


def get_soup(link):

    try:

        link = link.replace('\n','').strip()
        headers = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(link,headers=headers)

        if response.status_code == requests.codes.ok:
            page = response.content
            soup = BeautifulSoup(page, "lxml")

        else:
            soup = None
            print("Requests returned status_code: {0}. {1}".format(response.status_code,link))

        return soup

    except Exception as e:
        print(str(e))
        print(link)


def prepare_url(host,model_name):
    if model_name:
        url = '{0}api/{1}/update/'.format(host,model_name)
    else:
        url = '{0}api/update/_bulk'.format(host)
    return url


def prepare_headers(token,username,password,json):
    headers = {
        'Authorization': 'Token {0}'.format(token),
        'user': username,
        'password': password,
    }
    if json:
        headers['Content-Type'] = 'application/json'
    return headers


def update_or_create_model_instance(host,token,username,password,data,model_name=None,json=False):

    url = prepare_url(host,model_name)
    headers = prepare_headers(token,username,password,json)
    if json:
        payload = data
        response = requests.put(url,headers=headers,json=payload)
    else:
        response = requests.put(url,headers=headers,data=data)

    return response


def list_model_instances(host,token,username,password,data,model_name,query=None):

    url = prepare_url(host,model_name) + query
    json = None
    headers = prepare_headers(token,username,password,json)
    response = requests.put(url,headers=headers)

    return response


def get_first_name_last_name(raw_name):

    full_name = raw_name.strip().replace('  ',' ').strip()
    full_name_split = full_name.split()
    prepositional_articles = ['von', 'Von', 'VON', 'van', 'Van', 'VAN', 'de', 'De','di','Di','da','Da','du', 'Du', 'des', 'Des', 'del', 'Del', 'della', 'Della','in','In','le','Le','la','La']
    first_name = ''
    last_name = ''

    if len(full_name_split) == 2:
        first_name = full_name_split[0].strip()
        last_name = full_name_split[1].strip()
    else:
        for i in range(len(full_name_split)):
            if any(prepositional_article == full_name_split[i] for prepositional_article in prepositional_articles):
                first_name = raw_name.split(' ',i)[0].strip()
                last_name = raw_name.split(' ',i)[1].strip()
                break

    # If we still have not identified a first_name by this point then we should try
    # something different.
    if not first_name:
        if len(full_name_split) == 3:
            first_name = raw_name.rsplit(' ',1)[0].strip()
            last_name = raw_name.split(' ',2)[2].strip()
        elif len(full_name_split) == 4:
            first_name = raw_name.rsplit(' ',2)[0].strip()
            last_name = raw_name.split(' ',2)[2].strip()

    d = {
        'full_name': full_name,
        'first_name': first_name,
        'last_name': last_name,
    }

    return d


def get_full_name_with_capitalised_surname(raw_name):
    first_name = ''
    last_name = ''
    for word in raw_name.split():
        if word.isupper() and '.' not in word:
            last_name += '{0} '.format(word.strip())
        else:
            first_name += '{0} '.format(word.strip().capitalize())
    first_name = first_name.strip()
    last_name = last_name.strip().title()
    full_name = '{0} {1}'.format(first_name,last_name)

    d = {
        'full_name': full_name.strip(),
        'first_name': first_name,
        'last_name': last_name,
    }

    # If it didn't work then we should try another method.
    if not first_name or not last_name:
        d = get_first_name_last_name(raw_name)

    return d


def extract_full_text(contains_full_text):
    full_text = ''
    for paragraph in contains_full_text.findAll('p'):
        full_text += paragraph.text.strip()
        full_text += '\n'
    full_text = full_text.strip()
    return full_text


def get_link_from_xml_item(item):
    for element in item:
        if str(element).strip().startswith('http'):
            link = element.strip()
            return link


def get_clean_committee_name(committee_name):
    committee_name = committee_name.replace("Committee on ", "").replace("Committee on the ", "").replace("Special committee on","").replace("Subcommittee on ", "").replace("Committee of Inquiry into ", "").replace('(Associated committee)','').replace('Committtee','').replace('European Parliament','').strip()

    if committee_name.startswith("the "):
        clean_committee_name = committee_name[4:]

    elif committee_name == 'Committee of Inquiry to investigate alleged contraventions and maladministration in the application of Union law in relation to money laundering, tax avoidance and tax evasion':
        clean_committee_name = 'Money laundering, tax avoidance and tax evasion'

    else:
        clean_committee_name = committee_name

    if "Delegation" in clean_committee_name:
        clean_committee_name = 'EP {0}'.format(clean_committee_name)
    else:
        clean_committee_name = 'EP {0} Committee'.format(clean_committee_name)

    return clean_committee_name


def get_committee_pk_from_initials(initials):

    committees = {
        "AFET": 1,
        "DROI": 38291,
        "SEDE": 42,
        "DEVE": 44,
        "INTA": 46,
        "BUDG": 47,
        "CONT": 48,
        "ECON": 50,
        "EMPL": 51,
        "ENVI": 53,
        "ITRE": 55,
        "IMCO": 56,
        "TRAN": 57,
        "REGI": 59,
        "AGRI": 60,
        "PECH": 62,
        "CULT": 64,
        "JURI": 65,
        "LIBE": 67,
        "AFCO": 68,
        "FEMM": 70,
        "PETI": 71,
        "COP": 255,
        "TAX3": 161,   
        "TAXE": 153,
        "TAXE2": 184,
        "TERR": 115,
        "PEST": 93,
        "EMIS": 80,
        "PANA": 81,
    }
    pk = committees[initials]

    return pk


def extract_screen_name_from_link(link):

    if len(str(link.split('/')[3])) <= 16:
        screen_name = link.split('/')[3]

    elif len(str(link.split('/')[-1])) <=16 and len(str(link.split('/')[-1])) >=1:
        screen_name = link.split('/')[-1]

    else:
        screen_name = None

    return screen_name


def get_twiiter_id_str(screen_name,lambda_client):

    event = {
        "screen_name":screen_name,
    }
    response = lambda_client.invoke(
        FunctionName='twitterFunctions-getID',
        InvocationType='RequestResponse',
        Payload=json.dumps(event),
    )
    id_str = response['Payload'].read().decode("utf-8")
    
    return id_str


def generate_twitter_account(screen_name, person__pk, lambda_client, briefed_api_host,briefed_api_token,briefed_api_username,briefed_api_password):

    response = get_twiiter_id_str(screen_name, lambda_client)
    if 'errorMessage' in response:
        response_twitter_handle = (response,500)
    else:
        data = {
            'person': person__pk,
            'link': 'https://twitter.com/' + screen_name,
            'screen_name': screen_name,
            'twitter_id_str': response,
            "lambda": "scrapersNews-utils-2"
        }
        response = update_or_create_model_instance(briefed_api_host,briefed_api_token,briefed_api_username,briefed_api_password,data,model_name='common_entity_data')
        response_twitter_handle = (response.text,response.status_code)

    return response_twitter_handle


def get_root(url,ET):
    r = requests.get(url)
    root = ET.fromstring(r.content)
    return root


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
