from org.models import Org, OrgInvitation

def create_org(admin, name="Simpler Times"):
    # create the org
    org = Org.objects.create(name=name, admin=admin)
    
    # update the admin
    admin.orgs.add(org)
    admin.save()
    
    return org

def create_invitation(org, user):
    # create the invitation
    invitation = OrgInvitation.objects.create(org=org, invited_by=user)

    # update the user
    return invitation