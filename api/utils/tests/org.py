from org.models import Org

def create_org(admin, name="Simpler Times"):
    # create the org
    org = Org.objects.create(name=name, admin=admin)
    
    # update the admin
    admin.orgs.add(org)
    admin.save()
    
    return org