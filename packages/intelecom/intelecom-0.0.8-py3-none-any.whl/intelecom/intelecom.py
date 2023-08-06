'''
Module to handle IN operations
'''

import logging
import re
import socket

class INConnection():
    '''INConnection class'''

    def __init__(self, host, username, password, port, buffer_size):
        '''Initializes the INConnection setting the host and port'''
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.username = username
        self.password = password
        self.session_id = ''
        self.in_socket = None

    def __enter__(self):
        self.in_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.in_socket.connect((self.host, self.port))
        self.login()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''Destructor'''
        self.logout()
        self.in_socket.close()

    def login(self):
        '''Login to IN server'''
        response = self.execute_login_command('login|{0}|{1}'.format(
            self.username, self.password)
        )

        success_finder = re.compile(r'succeeded', re.IGNORECASE)

        if success_finder.search('{}'.format(response)):
            session_id_collector = re.compile(
                r'ACKLGN(?P<SESSION>[0-9]{8})', re.IGNORECASE
            )
            self.session_id = session_id_collector.findall(
                '{}'.format(response)
            )[0]
        else:
            raise INLoginError(
                'FAILED: IN login (username=%s, password=%s) - Response: %s',
                self.username,
                self.password
            )

    def logout(self):
        '''Logout of the IN session'''
        response = self.execute_command('logout|{0}'.format(self.username))

        success_finder = re.compile(r'succeeded', re.IGNORECASE)

        if not success_finder.search(f'{response}'):
            raise INLogoutError(
                'FAILED: IN Logout session(%s) - Response: %s',
                self.session_id,
                response)

    def reset_sim_password(self, msisdn):
        '''Reset password'''

        sim_password = '654321'
        response = self.execute_command(
            'MODI EPPC SIMPSWD:MSISDN={0},OPRPSWD={1},NEWPSWD={2},CFMPSWD={2};'.format(
                msisdn, self.password, sim_password
            )
        )

        success_finder = re.compile(r'RETN=0', re.IGNORECASE)

        if success_finder.search(f'{response}'):
            return True
        else:
            raise ResetSimPasswordError(
                'FAILED: MSISDN(%s) reset sim password - Response: %s',
                msisdn,
                response
            )

    def purchase_package(self, msisdn, package_type, package_grade):
        '''Purchase package'''

        sim_password = '654321'

        if self.reset_sim_password(msisdn):
            response = self.execute_command(
                'SET EPPC RESPKG:MSISDN={0},MSUBPSWD={1},PKGTYPE={2},' /
                'PKGGRADE={3};'.format(
                    msisdn,
                    sim_password,
                    package_type,
                    package_grade
                )
            )

            success_finder = re.compile(r'RETN=0', re.IGNORECASE)

            if success_finder.search(f'{response}'):
                return True

        raise ResetSimPasswordError(
            'FAILED: MSISDN(%s) purchase package (type=%s, grade=%s)' /
            ' - Response: %s',
            msisdn,
            package_type,
            package_grade,
            response
        )

    def change_profile(self, msisdn, profile):
        '''Change account profile'''

        response = self.execute_command(
            f'MODI EPPC USERTYPE:MSISDN={msisdn},USERTYPE={profile};'
        )

        success_finder = re.compile(r'RETN=0', re.IGNORECASE)

        if success_finder.search(f'{response}'):
            return True
        else:
            raise ChangeProfileError(
                'FAILED: Change msisdn(%s) profile to %s - Response: %s',
                msisdn,
                profile,
                response
            )

    def display_account_info(self, msisdn):
        '''Display account info'''
        response = self.execute_command(
            f'DISP EPPC ACNTINFO:MSISDN={msisdn},QUERYTYPE=1,QUERYSCP=1;'
        )

        success_finder = re.compile(r'RETN=2001', re.IGNORECASE)

        if success_finder.search(f'{response}'):
            raise MsisdnMatchError(
                'Invalid MSISDN %s - Response: %s',
                msisdn,
                response
            )

        success_finder = re.compile(r'RETN=0', re.IGNORECASE)

        if success_finder.search(f'{response}'):
            result_finder = re.compile(r'RESULT=".*"')
            values = re.split('=|"| & ', result_finder.findall(str(response))[0])[2:31]
            keys = [
                'MSISDN',
                'ACCLEFT',
                'LOCKFLG',
                'ACNTSTAT',
                'CLMFLG',
                'CALLINGROAMOUTFLG',
                'CALLEDROAMOUTFLG',
                'CLIALW',
                'OCSFLG',
                'CALLRANGE',
                'SERVICESTART',
                'ACCOUNTSTOP',
                'CALLSERVSTOP',
                'PREACCOUNTSTOP',
                'PREFREEZESTOP',
                'USERTYPE',
                'SUBSCRIBERTYPE',
                'USERFLG',
                'LANGUAGE',
                'SMLANGUAGE',
                'LIFECIRCLE',
                'MSFEE',
                'MSTOTALFEE',
                'MSMONTHDEDUCT',
                'BIRTHDAY',
                'ENTRYBLACKTIME',
                'DIALMOBILENUMFLG',
                'ANSCLCTCALLFLG',
                'TMPNUMFLG'
            ]

            account_info = zip(keys, values)

            return dict(account_info)

        raise INQueryError(
            'FAILED: IN account info display on %s - Response: %s',
            msisdn,
            response
        )

    def credit_account(self, msisdn, amount, reason):
        '''Credit account'''

        response = self.execute_command('MODI EPPC ACCOUNT:MSISDN={0},BALANCE={1},APPINFO={2};'.format(msisdn, amount, reason))

        success_finder = re.compile(r'RETN=0', re.IGNORECASE)

        if success_finder.search(f'{response}'):
            return True
        else:
            raise INCreditError(
                'FAILED: Credit msisdn (%s) amount %s - Response: %s',
                msisdn,
                amount,
                response
            )
            return False

    def debit_account(self, msisdn, amount, reason):
        '''Debit account'''

        response = self.execute_command('MODI EPPC ACCOUNT:MSISDN={0},BALANCE=-{1},APPINFO={2};'.format(msisdn, amount, reason))

        success_finder = re.compile(r'RETN=0', re.IGNORECASE)

        if success_finder.search(f'{response}'):
            return True
        else:
            raise INDebitError(
                'FAILED: Debit msisdn (%s) amount %s - Response: %s',
                msisdn,
                amount
            )

    def scratch_card_recharge(self, msisdn, recharge_code, reason):
        '''Recharge using scratch card'''
        response = self.execute_command('CARD EPPC ACNT: MSISDN={0},PPCCARDPIN={1},APPINFO={2}'.format(msisdn, recharge_code, reason))
        success_finder = re.compile(r'RETN=0', re.IGNORECASE)

        if success_finder.search(f'{response}'):
            return True
        else:
            raise ScratchCardRechargeError(
                'FAILED: MSISDN %s recharge scratch card %s - Response: %s',
                msisdn,
                recharge_code,
                response
            )

    def execute_command(self, command):
        '''Execute commands'''

        formatted_command = '{0}|{1}\r\n'.format(self.session_id, command)
        self.in_socket.send(formatted_command.encode())
        response = self.in_socket.recv(self.buffer_size)

        return response

    def execute_login_command(self, command):
        '''Execute login command'''

        logging.info('IN login command: %s', command)

        formatted_command = '{0}\r\n'.format(command)
        self.in_socket.send(formatted_command.encode())
        response = self.in_socket.recv(self.buffer_size)

        logging.info('IN login response: %s', response)

        return response


class BaseINError(ValueError):
    pass


class MsisdnMatchError(BaseINError):
    pass


class INQueryError(BaseINError):
    pass


class INLoginError(BaseINError):
    pass


class INLogoutError(BaseINError):
    pass


class INCreditError(BaseINError):
    pass


class INDebitError(BaseINError):
    pass


class PackagePurchaseError(BaseINError):
    pass


class ResetSimPasswordError(BaseINError):
    pass


class ChangeProfileError(BaseINError):
    pass


class ScratchCardRechargeError(BaseINError):
    pass
