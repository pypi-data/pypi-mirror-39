from scrapy.mail import MailSender
import datetime



class Notify_Stats:
    host = ''
    user = ''
    password = ''
    mail_from = ''
    ssl = True
    port = 0
    shub_url = ''
    nameSpider = ''
    def __init__(self,host, user, password, mail_from, is_ssl, port_number, shub_url, nameSpider, source_url):
        self.host = host
        self.user = user
        self.password = password
        self.mail_from = mail_from
        self.ssl = is_ssl
        self.port = port_number
        self.shub_url = shub_url
        self.nameSpider = nameSpider
        self.source_url = source_url

    def send_mail(self, data, notify_to, subject):
        html = '<html><head></head><body> ' \
               '         <table> ' \
               '             <tbody>'

        html2 = ''
        html3 = ''
        html4 = ''
        html5 = ''
        html7 = ''

        top_section = '   <tr>' \
                       '            <td style="width:330px">Spider name</td>' \
                       '            <td>' + self.nameSpider + '</td>' \
                                                              '        </tr>'
        top_section += '   <tr>' \
                       '            <td style="width:330px">Url source</td>' \
                       '            <td>' + self.source_url + '</td>' \
                                                              '        </tr>'


        error_section = ''
        scraping_duration = ''
        startime = ''
        for x in data:

            if (x[0:10] == 'downloader'):
                html2 += '             <tr>' \
                         '                 <td style="width:330px">%s </td>' \
                         '                 <td>%s</td>' \
                         '             </tr>' % (x, str(data[x]))

            elif (x[0:9] == 'scheduler'):
                html3 += '             <tr>' \
                         '                 <td style="width:330px">%s </td>' \
                         '                 <td>%s</td>' \
                         '             </tr>' % (x, str(data[x]))

            elif (x[0:8] == 'memusage'):
                html4 += '             <tr>' \
                         '                 <td style="width:330px">%s </td>' \
                         '                 <td>%s</td>' \
                         '             </tr>' % (x, str(data[x]))

            elif (x[0:8] == 'log_count'):
                html5 += '             <tr>' \
                         '                 <td style="width:330px">%s </td>' \
                         '                 <td>%s</td>' \
                         '             </tr>' % (x, str(data[x]))

            elif (x[:5] == "Error" or x[:5] == "error" or x[:5] == "ERROR"):
                error_section += '    <tr style="color: red; font-weight: bold; padding-left: 50px">' \
                                 '                 <td style="width:330px">%s </td>' \
                                 '                 <td>%s</td>' \
                                 '             </tr><tr><td><div style="color: grey; width: 400px">________________________________________</div></td></tr>' % (
                                     x, str(data[x]))
            elif (x == "item_to_be_scraped"):
                top_section += '       <tr>' \
                               '                 <td style="width:330px">Number of items to be scrapped</td>' \
                               '                 <td>%s</td>' \
                               '             </tr>' % str(data[x])

            elif (x == "item_scraped_count"):
                top_section += '       <tr>' \
                               '                 <td style="width:330px">Number of items created (single locations)</td>' \
                               '                 <td>%s</td>' \
                               '             </tr>' % str(data[x])
            elif (x == "start_time"):
                startime = '      <tr>' \
                               '                 <td style="width:330px">Start time </td>' \
                               '                 <td>%s</td>' \
                               '             </tr>' % str(data[x].strftime("%Y-%m-%d %H:%M:%S"))
                scraping_duration = datetime.datetime.now() - data[x]
            else:
                html7 += '             <tr>' \
                         '                 <td style="width:330px">%s </td>' \
                         '                 <td>%s</td>' \
                         '             </tr>' % (x, str(data[x]))


        tech_section = html2 + html3 + html4 + html5 + html7

        top_section = top_section+startime+' <tr>' \
                       '                 <td style="width:330px">Scraping duration</td>' \
                       '                 <td>%s <span style="color:grey; padding-left:15px">[hours:minute:seconds]</span> </td>' \
                       '       </tr>' % datetime.timedelta(
            seconds=scraping_duration.seconds)
        top_section += '  <tr>' \
                      '            <td style="width:330px">Url scrapinghub job</td>' \
                      '            <td>'+self.shub_url.replace(" ","")+'</td>' \
                      '        </tr><tr><td><div style="color: grey; width: 400px">________________________________________</div></td></tr>'

        if error_section:
            html += top_section + error_section + tech_section
        else:
            html += top_section + tech_section

        html += '         </tbody></table>' \
                '     </body></html>'
        try:
            mailer = MailSender(smtphost=self.host, smtpuser=self.user, smtppass=self.password,
                                mailfrom=self.mail_from, smtpssl=self.ssl, smtpport=self.port)
            mailer.send(to=notify_to, subject=subject, body=html,  mimetype='text/html')
        except Exception as e:
            print(e)