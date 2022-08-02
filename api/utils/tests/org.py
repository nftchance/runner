from org.models import ADMIN, CUSTOMER, Org, OrgInvitation, OrgRelationship

def create_org(admin, name="Simpler Times"):
    # create the org
    org = Org.objects.create(name=name, admin=admin)
    
    # create the admin relationship
    relationship, created = OrgRelationship.objects.get_or_create(
        org=org, related_user=admin, relationship=ADMIN
    )

    # update the admin
    admin.org_relationships.add(relationship)
    admin.save()
    
    return org

def create_invitation(org, user, relationship=CUSTOMER):
    # create the invitation
    invitation = OrgInvitation.objects.create(org=org, invited_by=user, relationship=relationship)

    # update the user
    return invitation