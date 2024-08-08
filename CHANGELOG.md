# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fix rare issue where GP2GP Large Message compressed fragments were being corrupted by the inbound adaptor.

## [1.3.1] - 2023-11-22

### Fixed

- Removed logging of inbound request data at ERROR level.
  This appears to have been accidently added in version 1.2.4 as part of debugging, but has the side effect of duplicating request data in the logs.
  This additional log was erroneously output at ERROR level, and slows down the adaptor.

## [1.3.0] - 2023-10-23

### Added

- Added support for new GP2GP interaction RCMR_IN030000UK07

## [1.2.9] - 2023-10-19

### Changed 

- Remove the SUPPORTED_FILE_TYPES environment variable.
  As the allowed types are fixed by the Spine External Interface Specification. 

### Fixed
- Messages sent to the inbound AMQP are configured with durability enabled.
  This should cause the broker to try its hardest to keep the message, e.g. in the event of a reboot.
  Some brokers (e.g. RabbitMQ) will need to have the existing non-durable queue deleted before a durable version can be created.

## [1.2.8] - 2023-09-20

### Fixed

Fix issue where MHS adaptor does not accept more than 98 external attachments

## [1.2.7] - 2023-09-18

### Fixed

Fix issue where inbound messages containing multibyte UTF-8 characters are mangled.

## [1.2.2] - 2022-04-21

### Changed

Security updates

## [1.2.1] - 2022-03-11

### Changed

Lowering logging level to not expose security headers

## [1.2.0] - 2022-03-02

### Changed

Support using SDS API instead of Spine Route Lookup allowing to use MHS without LDAP connectivity. 

## [1.1.1] - 2021-09-15

### Changed

NIAD-1714: To support any description on attachments #82

## [1.1.0] - 2021-08-09

### Changed

NIAD-924: Rename to better reflect fields purpose (#73)
Make docker build tags optional arguments (#62)
ReadMe updates for MHS (#26)
NIAD-1485: Dependencies updated (#69)
NIAD-1286: Enabling external attachments in forward-reliable (#59)
NIAD-1443-MHS-Add-VPCEndpoint-For-Secrets-Manager-API (#61)
NIAD-1055 Added script to test inbound endpoint to help diagnose conn… (#58)
NIAD-1099 Test script fixes for MacOS (#57)
Update README.md to add known limitations of secrets / key vault (#56)
NIAD-1099 test script improvements (#48)
Changes to several pieces required for inbound to properly process sp… (#55)
Remove old terraform-kubernetes, update state bucket code, update bas… (#39)
Readme file for MHS Azure deployment (#42)

## [1.0.2] - 2020-12-09
 
### Changed
- Fix not sending attachments to Spine in Forward-Reliable workflow

## [1.0.0] - 2020-07-14

### Added
- A pre-assured MHS adaptor
 
### Changed
