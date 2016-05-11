# Load the jinja library's namespace into the current module.
import jinja2

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
TEMPLATE_FILE = "/home/tom/Documents/Topo/scraper/template.html"

# Read the template file using the environment object.
# This also constructs our Template object.
template = templateEnv.get_template( TEMPLATE_FILE )

# Specify any input variables to the template as a dictionary.
templateVars = { "title" : "Test Example",
                 "number" : "1",
                 "name" : "Boulder",
                 "opener" : "Tony",
                 "type" : "overhang",
                 "info" : "dont use the jug",
                 "list" : [1,2,3] }

# Finally, process the template to produce our final text.
outputText = template.render( templateVars )

htmlfile=open('boulders.html','w')
htmlfile.write(outputText)
htmlfile.close()
