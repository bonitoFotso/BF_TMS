# Generated by Django 3.2.20 on 2023-08-21 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tache',
            options={'ordering': ['createdAt'], 'verbose_name': 'Tache', 'verbose_name_plural': 'Taches'},
        ),
        migrations.AddField(
            model_name='tache',
            name='appelant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='clients.appelant', verbose_name='Celui qui appelle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tache',
            name='n_OS',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Numéro d'OS"),
        ),
        migrations.AddField(
            model_name='tache',
            name='type_intervention',
            field=models.CharField(choices=[('videosurveillance', 'Vidéosurveillance'), ('controle_acces', "Contrôle d'accès"), ('systeme_incendie', 'Système incendie'), ('intrusion', 'Intrusion'), ('dab', 'DAB (Distributeur automatique de billets)')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tache',
            name='intervention',
            field=models.CharField(choices=[('maintenance', 'Maintenance'), ('installation', 'Installation'), ('incident', 'Incident'), ('survey', 'Enquête'), ('extension', 'Extension'), ('migration', 'Migration')], max_length=20),
        ),
        migrations.AlterField(
            model_name='tache',
            name='nom',
            field=models.CharField(max_length=50, null=True, verbose_name='n'),
        ),
        migrations.AlterField(
            model_name='tache',
            name='priorite',
            field=models.CharField(choices=[('Bas', 'Bas'), ('Moyen', 'Moyen'), ('Élevé', 'Élevé')], default='appelant', max_length=20),
        ),
        migrations.AlterField(
            model_name='tache',
            name='status',
            field=models.CharField(choices=[('En attente', 'En attente'), ('En cours', 'En cours'), ('En arrêt', 'En arrêt'), ('En facturation', 'En facturation')], default='En attente', max_length=20),
        ),
    ]
