# Disposable Email Domain List

This is a list of domains used by temporary or disposable email services.

This list is daily updated and validated by MX scan. It's made as short as possible.

# Download

You can download this list in [TXT format](https://raw.githubusercontent.com/yzyjim/disposable-email-domain-list/master/domains.txt) or [JSON format](https://raw.githubusercontent.com/yzyjim/disposable-email-domain-list/master/domains.json).

# What is disposable email?

[Disposable email addresses](http://en.wikipedia.org/wiki/Disposable_email_address) are known as DEA or dark mail. It is a kind of service that generates a unique or random email address that is used for every contact or entity.

This repository includes a collection of domains that are used by the disposable email services that are still functioning at the time of the validation.

The administrators could use this list to prevent potentially fraudulent activities.

# Approach

This list is periodically retrieved and validated by scanning the MX records. Only the domains that still had MX records were kept in this list. Duplicated items were removed. Therefore, this list has been made as short as possible.

![demo.gif](demo.gif?raw=true)

# Source

The raw data was periodically collected from these repositories:

- [ivolo/disposable-email-domains](https://github.com/ivolo/disposable-email-domains)
- [michenriksen/disposable-email-provider-domains](https://gist.github.com/michenriksen/8710649)
- [martenson/disposable-email-domains](https://github.com/martenson/disposable-email-domains)
- [GeroldSetz/emailondeck.com-domains](https://github.com/GeroldSetz/emailondeck.com-domains)

# Usage

If you want to build such a list on your own, run `main.php` to automatically retrieve and sanitize raw data and validate these domains. It will take hours. The validated domains will be stored in `domains.txt`.

# Contribution

This repository does not accept contribution of new domains because it simply retrieves and cleans data from the sources listed above. However, you can, for example, add new disposable domains to ivolo's [disposable-email-domains](https://github.com/ivolo/disposable-email-domains) repository. Read its [contributing section](https://github.com/ivolo/disposable-email-domains#contributing) for details.

# License

This project is licensed under the MIT License - read the [LICENSE](LICENSE) file for details.

