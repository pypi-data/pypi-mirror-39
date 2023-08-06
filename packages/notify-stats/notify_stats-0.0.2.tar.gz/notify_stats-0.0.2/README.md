# notify_stats

This is a sample code to use this package.

from notify_stats import notify_stats

notify = notify_stats(\
           host="host",\
           user="user",\
           password="password",\
           mail_from="from_email",\
           port_number= post,\
           is_ssl=True/False,\
           shub_url='link_to_cloud',\
           nameSpider='your_spider_name',\
           source_url='source_link'\
        )

notify.send_mail(data=spider.crawler.stats.get_stats(),notify_to=list_of_email(s), subject="your_subject")))

Requirement: MailSender