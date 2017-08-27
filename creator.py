import jinja2
import codecs

def create_topo(area):

    print()
    print("Creating the topo")

    # In this case, we will load templates off the filesystem.
    # This means we must construct a FileSystemLoader object.
    # 
    # The search path can be used to make finding templates by
    #   relative paths much easier.  In this case, we are using
    #   absolute paths and thus set it to the filesystem root.
    templateLoader = jinja2.FileSystemLoader( searchpath="/" )

    # An environment provides the data necessary to read and
    #   parse our templates.  We pass in the loader object here.
    templateEnv = jinja2.Environment( loader=templateLoader )

    # This constant string specifies the template file we will use.
    TEMPLATE_FILE = "/home/tom/Software/bleau-scraper/template.html"

    # Read the template file using the environment object.
    # This also constructs our Template object.
    template = templateEnv.get_template( TEMPLATE_FILE )

    # Specify any input variables to the template as a dictionary.
    templateVars = { "title"  : area.getName(),
           "road"     : area.getInfo(),
           "list"     : area.getTopolist(),
           "numb"     : [x['numb'] for x in area.boulder_list],
           "name"     : [x['name'] for x in area.boulder_list],
           "grad"     : [(', ').join(x['grade']) for x in area.boulder_list],
           "open"     : [(', ').join(x['opener']) for x in area.boulder_list],
           "type"     : [(', ').join(x['style']) for x in area.boulder_list],
           "info"     : [x['info'] for x in area.boulder_list],
           "reps"     : [x['ascents'] for x in area.boulder_list],
           "numb_popu": [x['numb'] for x in area.popularBoulders()][:10],
           "name_popu": [x['name'] for x in area.popularBoulders()][:10],
           "grad_popu": [(', ').join(x['grade']) for x in area.popularBoulders()][:10],
           "reps_popu": [x['ascents'] for x in area.popularBoulders()]}

    # Finally, process the template to produce our final text.
    outputText = template.render( templateVars )

    htmlfile=codecs.open(area.getName().replace(' ','')+'.html','w',encoding='utf-8')
    htmlfile.write(outputText)
    htmlfile.close()

