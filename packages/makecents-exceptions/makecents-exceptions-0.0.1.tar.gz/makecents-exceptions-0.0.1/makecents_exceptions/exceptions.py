###############################################################
#   (c) 2017 Makecents LLC
#   Created by Thomas Veale
#   Purpose: Defines a set of custom errors for specific types
#       of failures.
#   License: see LICENSE
###############################################################

import inspect
import sys


class MakecentsValueError(ValueError):
    code = None
    title = None
    message = None

    def to_dict(self):
        return {
            "code": self.code,
            "title": self.title,
            "message": self.message
        }


class ValidationError(MakecentsValueError):
    # TODO: follow this style
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class MissingCredentials(MakecentsValueError):
    pass


class BalanceNotFound(MakecentsValueError):
    def __repr__(self):
        return "Failed to retrieve makecents balance."


class FailedAuthentication(MakecentsValueError):
    code = 1
    title = 'Invalid Identity'
    message = 'They keys you are attempting to use have either been revoked or it do not exist.'


class StaleSignature(MakecentsValueError):
    code = 2
    title = 'Stale Signature'
    message = 'The signature you provided is stale.'


class InvalidSignature(MakecentsValueError):
    code = 3
    title = 'Invalid Signature'
    message = 'The signature you provided is invalid.'


class InvalidPayload(MakecentsValueError):
    code = 4
    title = 'Invalid Payload'
    message = 'Your request payload is either invalid or malformed.'


class InvalidPhoneNumber(MakecentsValueError):
    code = 5
    title = 'Invalid Phone Number'
    message = 'The phone number you have entered is not a valid mobile phone number.'


class InvalidVerificationCode(MakecentsValueError):
    code = 6
    title = 'Invalid Verification Code'
    message = 'The verification code you provided did not correlate with the expected on on the server.'


class InvalidProfileUpdate(MakecentsValueError):
    code = 7
    title = 'Invalid Profile Update'
    message = 'The update you are requesting is malformed.'


class InvalidEndpoint(MakecentsValueError):
    code = 10
    title = 'Invalid Endpoint'
    message = 'The endpoint or resource you are request does not exist.'


class InvalidTransactionID(MakecentsValueError):
    code = 11
    title = 'Invalid Transaction ID'
    message = 'The transaction you are looking for does not exist.'


class FailedPINAuthentication(MakecentsValueError):
    code = 12
    title = 'Invalid PIN'
    message = 'The PIN you provide is incorrect.'

    def __init__(self, allow_retry_times):
        self.allow_retry_times = allow_retry_times

    def to_dict(self):
        result = super().to_dict()
        result.update({
            "allow_retry_times": self.allow_retry_times
        })
        return result


class InvalidPINVerify(MakecentsValueError):
    code = 13
    title = 'Invalid PIN Verify'
    message = 'The PIN verification you are requesting is malformed.'


class InvalidPINUpdate(MakecentsValueError):
    code = 14
    title = 'Invalid PIN Update'
    message = 'The update you are requesting is malformed.'


class TooManyPINAttempt(MakecentsValueError):
    code = 15
    title = 'Too many PIN attempts'
    message = 'You have exceeded the allowable retry attempts.'


class InvalidStateAddr(MakecentsValueError):
    code = 16
    title = 'Invalid State Addr'
    message = 'The state address received is invalid.Please check again'


class InvalidEmail(MakecentsValueError):
    code = 17
    title = 'Invalid Email address'
    message = 'The email address you typed is invalid.Please check again'


class InvalidName(MakecentsValueError):
    code = 18
    title = 'Invalid user name'
    message = 'The name you entered is invalid.Please check again'


class InvalidCity(MakecentsValueError):
    code = 19
    title = 'Invalid user name'
    message = 'The name you entered is invalid.Please check again'


class InvalidCountry(MakecentsValueError):
    code = 21
    title = 'Invalid user name'
    message = 'The name you entered is invalid.Please check again'


class InvalidBank(MakecentsValueError):
    code = 22
    title = 'Invalid bank name'
    message = 'The bank name you entered is invalid.Please check again'


class InvalidPostalCode(MakecentsValueError):
    code = 23
    title = 'Invalid postal code'
    message = 'The postal code you entered is invalid.Please check again'


class InvalidBankAccount(MakecentsValueError):
    code = 24
    title = 'Invalid bank account number'
    message = 'The bank account number you entered is invalid.Please check again'


class InvalidRoutingNumber(MakecentsValueError):
    code = 25
    title = 'Invalid routing number'
    message = 'The routing number you entered is invalid.Please check again'


class InvalidAPIKey(MakecentsValueError):
    code = 26
    title = 'Invalid API key'
    message = 'The API key is invalid.Please check again'


class InvalidAPISec(MakecentsValueError):
    code = 27
    title = 'Invalid API sec'
    message = 'The API sec is invalid.Please check again'


class InvalidNonce(MakecentsValueError):
    code = 28
    title = 'Invalid Nonce'
    message = 'The Nonce you entered is invalid.Please check again'


class InvalidPairingId(MakecentsValueError):
    code = 29
    title = 'Invalid Pairing Id'
    message = 'The pairing id is invalid.Please check again'


class InvalidSenderName(MakecentsValueError):
    code = 30
    title = 'Invalid Sender Name'
    message = 'The Sender Name is invalid.Please check again'


class InvalidReceiverName(MakecentsValueError):
    code = 31
    title = 'Invalid Receiver Name'
    message = 'The Receiver Name is invalid.Please check again'


class InvalidTransactionValueType(MakecentsValueError):
    code = 32
    title = 'Invalid Transaction Value type'
    message = 'The Transaction Value Type is invalid.Please check again'


class InvalidBatchId(MakecentsValueError):
    code = 33
    title = 'Invalid Batch Id'
    message = 'The Batch Id is invalid.Please check again'


class InvalidOTP(MakecentsValueError):
    code = 34
    title = 'Invalid OTP'
    message = 'The OTP is invalid or outdated. Please check again'


class InvalidLocation(MakecentsValueError):
    code = 34
    title = 'Invalid Location'
    message = 'The Location is invalid. Please check again'


class InvalidInvoiceNumber(MakecentsValueError):
    code = 34
    title = 'Invalid Invoice Number'
    message = 'The Invoice Number is invalid or existing. Please check again'


class InvalidCashierId(MakecentsValueError):
    code = 34
    title = 'Invalid CashierId'
    message = 'The CashierId is invalid. Please check again'


class InvalidSearch(MakecentsValueError):
    code = 35
    title = 'Invalid Search'
    message = 'The search query is malformed'


class InvalidCashierName(MakecentsValueError):
    code = 36
    title = 'Invalid Cashier Name'
    message = 'The Cashier Name can not be empty. Please check again.'


class InvalidInsertError(MakecentsValueError):
    code = 37
    title = 'Invalid Database Insert'
    message = 'The row already exists in the table. Please check again.'


class NoEntriesFoundError(MakecentsValueError):
    code = 38
    title = 'No Entries Found'
    message = 'There does not seem to be any database entries. Please check your request.'


class FailedToCreateUser(MakecentsValueError):
    code = 39
    title = 'Failed to create User'
    message = 'Failed to create user and populate the profile. Please check again.'


class FileDoesNotExist(MakecentsValueError):
    code = 40
    title = 'File Does Not Exist'
    message = 'The file you are trying to access does not exist in this location. Please check it again'


class InvalidFileType(MakecentsValueError):
    code = 41
    title = 'Invalid File Type'
    message = 'The file you are trying to upload is of invalid type. Please upload a different file'


class InternalServiceError(MakecentsValueError):
    code = 20
    title = 'Generic Internal Service Error'
    message = 'Something is broken internally and should be reported.'


class UserDNE(MakecentsValueError):
    code = 99
    title = 'User DNE'
    message = 'The user you are attempting to send funds to does not exist.'
