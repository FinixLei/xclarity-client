from xclarityclient import client


def main():
    c = client.Client(version='xclarity_1.2.2',
                      username='USERID',
                      password='Passw0rd',
                      url='http://www.google.com')
    c.info()


if __name__ == '__main__':
    main()
