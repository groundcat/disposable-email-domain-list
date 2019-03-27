# Disposable Email Domain List

In `domains.txt` is a validated, cleaned, and up-to-date list of domains used by temporary and disposable email services that are still functioning at the time of the validation.

# What is disposable email?

[Disposable email addresses](http://en.wikipedia.org/wiki/Disposable_email_address) are known as DEA or dark mail. It is a kind of service that generates a unique or random email address that is used for every contact or entity.

This repository includes a collection of domains that are used by the disposable email services.

The administrators could use this list to prevent potentially fraudulent activities.

# Approach

This list has been validated by scanning the MX records. Only the domains that still had valid MX records were kept in this list. Duplicated items were removed. Therefore, this list has been made as short as possible.

# Source

The raw data was periodically collected from the following sources:

- [disposable-email-domains](https://github.com/ivolo/disposable-email-domains)
- [disposable-email-provider-domains](https://gist.github.com/michenriksen/8710649)

# Usage

If you want to build such a list on your own, run `main.php` to automatically retrieve and sanitize raw data and validate these domains. It will take hours. The validated domains will be stored in `domains.txt`.

# Contribution

This project does not accept contribution of new domains because it simply retrieves and cleans data from the sources listed above. You can add new disposable domains to ivolo's [disposable-email-domains](https://github.com/ivolo/disposable-email-domains) repository. Read its [contributing section](https://github.com/ivolo/disposable-email-domains#contributing) for details.

