env = {}

with open('../../.env', 'r') as file:
    for line in file:
        if '=' in line:
            item = line.split('=')
            env[item[0]] = item[1].strip('\n')

config = """
input {{
  jdbc {{
    jdbc_connection_string => "jdbc:postgresql://db:5432/{0}"
    jdbc_user => "{1}"
    jdbc_password => "{2}"
    jdbc_driver_library => "/usr/share/java/postgresql-42.2.6.jar"
    jdbc_driver_class => "org.postgresql.Driver"
    schedule => "* * * * *"
    statement => "SELECT id, text, name FROM post"
    add_field => {{
      "table" => "post"
    }}
    jdbc_paging_enabled => "true"
    jdbc_page_size => "10000"
  }}
}}
filter {{
  if ([id]) {{
     mutate {{
       add_field => {{
         "[@metadata][document_id]" => "%{{id}}"
       }}
     }}
  }}
}}
output {{
  elasticsearch {{
    template_name => "posts"
    index => "%{{table}}-%{{+YYYY.MM.dd.HH.mm}}"
    hosts => ["elasticsearch:9200"]
    template => '/etc/logstash/conf.d/template.json'
    document_id => "%{{table}}_%{{[@metadata][document_id]}}"
  }}
}}
""".format(env['POSTGRES_DB'], env['POSTGRES_USER'], env['POSTGRES_PASSWORD'])

with open('config.conf', 'w') as file:
    file.write(config)
