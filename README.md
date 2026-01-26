Semester Project Requirements Document

Project Title: SecureSwipe

Developer Name: Garrett Kilgore


Business Context:

The prominent reason for a system like this one to exist is to have a reliable, but quick, credit card processor that allows for quick and easy transactions to all of the local and global banks with your credit card information being protected. Scammers are finding smarter ways to get ahold of our information, so we need a reliable and efficient way to keep this information safe and easy to use. Our system will keep users' information safe and will protect them from fraud scammers that are trying to trick them into giving them money, without overly complicating the process of using your credit card.


Problem Statement:

The problem that this solution is attempting to solve is to provide everyone a fast and easy way to take care of their transactions while also keeping them away from scammers that are finding newer and better ways to creep around most other securities that get people’s credit card information. It is important to find a good balance between being too simple to the point where any scammer could get ahold of someone’s information, and at the same time, being too overly complicated to the point where hardly anyone will use it. Users need to be notified when something is wrong and they are potentially being scammed by someone.


Scope:

The application will contain several ways of detecting fraud and preventing a user from giving that scammer some money. Some of the ways this will work would be by detecting if the amount of money being sent is absurdly high, some of the information being entered is incorrect, if a card is being used passed its expiration date, and potentially sending the card holder an email letting that person know that he or she might be getting scammed. However this last detail might be in a future release.


Functional Requirements:

1. The application needs to require a certain amount of information for a card to be accepted but at the same time, not overdo the amount of information needed which will result in a lot of declines.

2. The format will be the card holder’s name, address, card number, expiration date, the ccv, and the amount spent. There will be some optional info like a phone number.

3. All of the card holder’s info will be stored into an organized database.

4. There will be an alert if a piece of info is invalid.

5. There will be a way to update/change a person’s information if he or she got a new credit card or changed location.

6. The system will be able to review or provide a list of previous transactions for auditing.

7. The system will reject requests that are asking for a very high amount of money.

8. The system will be able to identify duplicate requests and bring up a window letting the user know it’s the same transaction a 2nd time.

9. The system will forward the request to the correct bank.

10. The system will detect when a card is used multiple times within a short time window and flag the activity as potential fraud.

11. The system will flag any activity that involves a card being used by someone under a different name.

12. The system will detect if the card is being used past its expiration date.

13. A fraud message will pop up if any of the system’s fraud alerts go off.

14. The system will have a fraud section on the database to list if a card has been flagged or involved with any fraud that the system might pick up on

15. If there is a very high frequency of transactions from the same location, the system can flag this as potential fraud.

16. The system will detect when a merchant submits transactions with missing or inconsistent metadata and classify them as suspicious.

17. The application will send out an email to the cardholder about potential fraud.


Non-Functional Requirements:

1. The application will switch to backup servers if the main servers go down to keep the service going.

2. There will be logs of all of the fraud banks out there that the system will instantly deny.

3. This application will support multiple merchants and multiple bank/card providers without requiring code changes.

4. Only authorized merchants will be allowed to submit transactions, enforced through an authentication mechanism.

5. The application will support a test mode that allows developers to simulate transactions without affecting account balances.

6. The system will use memory, CPU, and network resources efficiently to support multiple concurrent requests.

7. The system will have a face scanner that will ask the user to upload a photo with their drivers license to verify that the user exists.

8. Only authorized users may view or retrieve fraud‑alert logs.

9. The system must continue operating even when fraud‑related fields are missing or invalid.

10. Logging suspicious activity must not significantly slow down transaction processing.

11. Rules must be tuned to avoid unnecessary declines in the simulation environment.
