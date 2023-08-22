from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from datetime import date,datetime
from django.utils import timezone
from apps.authentication.models import User 
from apps.clients.models import *

def generate_matricule():
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    
    last_technicien = Technicien.objects.order_by('-id').first()
    
    if last_technicien:
        last_matricule = last_technicien.matricule
        last_num = int(last_matricule.split("-")[-1])
        new_num = last_num + 1
    else:
        new_num = 1
        
    matricule = f'{year}-{month}-{new_num:04}'
    return matricule


class Technicien(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE,null=True)
    photo = models.ImageField(_("profile"), upload_to='media/profile',default='media/profile/ims.jpg' )
    nom  = models.CharField(_("nom"), max_length=50)
    prenom = models.CharField(_("prenom"), max_length=50)
    tel = models.CharField(_("telephone"),max_length=20)
    email = models.EmailField(max_length=254)
    matricule = models.CharField(_("matricune"), unique=True,max_length=20)
    date_add = models.DateTimeField(auto_now_add=True) 
    date_upd = models.DateTimeField(auto_now=True)
    vitesse_execution = models.FloatField(_("Vitesse d'exécution"), default=0.0)
    efficacite = models.FloatField(_("Efficacité"), default=0.0)
    
    def __str__(self):
        return self.nom
    
    
    class Meta:
        
        managed = True
        verbose_name = 'Technicien'
        verbose_name_plural = 'Techniciens'

@receiver(pre_save, sender=Technicien)
def set_technicien_matricule(sender, instance, **kwargs):
    if not instance.matricule:
        instance.matricule = generate_matricule()

class Tache(models.Model):
    # Choix pour le champ 'intervention'
    INTERVENTION_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('installation', 'Installation'),
        ('incident', 'Incident'),
        ('survey', 'Enquête'),
        ('extension', 'Extension'),
        ('migration', 'Migration'),
    ]

    # Choix pour le champ 'type_intervention'
    TYPE_INTERVENTION_CHOICES = [
        ('videosurveillance', 'Vidéosurveillance'),
        ('controle_acces', 'Contrôle d\'accès'),
        ('systeme_incendie', 'Système incendie'),
        ('intrusion', 'Intrusion'),
        ('dab', 'DAB (Distributeur automatique de billets)'),
    ]

    # Choix pour le champ 'status'
    STATUS_CHOICES = [
        ('En attente', 'En attente'),
        ('En cours', 'En cours'),
        ('En arrêt', 'En arrêt'),
        ('En facturation', 'En facturation'),
    ]
    PRIORITE_CHOICES = [
    ('Bas', 'Bas'),
    ('Moyen', 'Moyen'),
    ('Élevé', 'Élevé'),
]


    nom = models.CharField(_("n"), max_length=50, null=True)
    intervention = models.CharField(choices=INTERVENTION_CHOICES, max_length=20)  # Choix d'intervention
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="En attente")  # Choix de statut
    type_intervention = models.CharField(choices=TYPE_INTERVENTION_CHOICES, max_length=20)  # Choix de type d'intervention
    appelant = models.ForeignKey(Appelant, verbose_name=_("Celui qui appelle"), on_delete=models.CASCADE)
    priorite = models.CharField(choices=PRIORITE_CHOICES, max_length=20,default='appelant')  # Choix de priorité
    description = models.CharField(max_length=500, null=False, default='description')
    n_OS = models.CharField(_("Numéro d'OS"), max_length=50, null=True, blank=True)
    ok = models.BooleanField(default=False)  # Champ pour indiquer si la tâche est terminée
    date_debut = models.DateField(_("Date de début"), blank=True, null=True)
    date_fin = models.DateField(_("Date de fin"), blank=True, null=True)
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique
    updatedAt = models.DateTimeField(auto_now_add=True)  # Date de mise à jour automatique

    def update_status(self):
        if self.technicientache_set.exists():
            self.status = 'En cours'
        else:
            self.status = 'En attente'
        self.save()
        
    def save(self, *args, **kwargs):
        # Définition du champ "nom" en fonction des valeurs des champs "intervention", "type_intervention" et "createdAt"
        self.n = f"{self.intervention} - {self.type_intervention} - {self.appelant}"
        if not self.nom:
            self.nom = slugify(self.n)
        super(Tache, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.nom  # Renvoie le nom unique de la tâche comme représentation en chaîne


    def get_agence(self):
        agence = self.appelant.agence
        return agence
    agence = property(get_agence)

    
    class Meta:
        verbose_name = _("Tache")
        verbose_name_plural = _("Taches")
        ordering = ['createdAt']

class TechnicienTache(models.Model):
    technicien = models.ForeignKey(Technicien, on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    ok = models.BooleanField(default=False)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)

class Rapport(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    num_os = models.CharField(_("Numéro d'OS"), max_length=50, null=True, blank=True)
    techniciens = models.ManyToManyField(Technicien, verbose_name=_("Techniciens ayant effectué la tâche"))
    rapport_text = models.TextField(_("Rapport"))
    date_creation = models.DateTimeField(auto_now_add=True)
    # ... autres champs du rapport ...

    def __str__(self):
        return f"Rapport pour {self.tache.nom}"

    def get_techniciens_list(self):
        return ", ".join([technicien.nom for technicien in self.techniciens.all()])

@receiver(post_save, sender=Tache)
def update_ok_status(sender, instance, **kwargs):
    technicien_taches = TechnicienTache.objects.filter(tache=instance, ok=True)
    instance.ok = any(technicien_tache.ok for technicien_tache in technicien_taches)
    instance.save()

@receiver(post_save, sender=TechnicienTache)
def update_status_tache(sender, instance, created, **kwargs):
    if created:
        tache = instance.tache
        tache.date_debut = instance.date_debut
        tache.status = 'En cours'
        tache.save()

class Action(models.Model):
    TACHE_ACTION_CHOICES = [
        ('creation', 'Création'),
        ('attribution', 'Attribution'),
        ('effectuation', 'Effectuation'),
    ]

    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    action_type = models.CharField(choices=TACHE_ACTION_CHOICES, max_length=20)
    date = models.DateField(auto_now_add=True)
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_action_type_display()} - {self.tache.nom}"
