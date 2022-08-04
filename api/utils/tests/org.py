from org.models import Org, OrgInvitation, OrgRelationship, OrgRole
from org.utils import Role

def create_org(admin, name="Simpler Times"):
    # create the org
    org = Org.objects.create(name=name, admin=admin)
    
    # get the admin role object
    role_obj = OrgRole.objects.get_or_create(name=Role.ADMIN)[0]

    # create the admin relationship
    relationship = OrgRelationship.objects.get_or_create(
        org=org, related_user=admin, role=role_obj
    )[0]

    # update the admin
    admin.org_relationships.add(relationship)
    admin.save()
    
    return org

def create_invitation(org, user, role=Role.CUSTOMER):
    # create the invitation
    invitation = OrgInvitation.objects.create(org=org, invited_by=user, role=role)

    # update the user
    return invitation