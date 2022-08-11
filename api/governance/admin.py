from django.contrib import admin

from .models import Proposal, ProposalVote


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    fields = ('proposed_by', 'votes', 'title', 'description', 'summary',
              'tags', 'closed_at', 'created_at', 'updated_at')
    readonly_fields = ('closed_at', 'created_at', 'updated_at')


@admin.register(ProposalVote)
class ProposalVoteAdmin(admin.ModelAdmin):
    fields = ('voter', 'vote', 'amount', 'created_at')
    readonly_fields = ('created_at',)
