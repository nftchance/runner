from django.db import models

class ProposalVote(models.Model):
    """
    A vote on a proposal.
    """
    voter = models.ForeignKey('user.User', on_delete=models.CASCADE)
    vote = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.proposal} - {self.voter} - {self.vote}'

class Proposal(models.Model):
    proposed_by = models.ForeignKey('user.User', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()

    votes = models.ManyToManyField(ProposalVote)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[RP{self.id}]"

    class Meta:
        ordering = ['-created_at']