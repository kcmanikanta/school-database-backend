from django.db import models

class StudentClass(models.Model):
    class_name = models.CharField(max_length=100, primary_key=True, help_text='Eg- Third, Fourth, Sixth etc')
    section = models.CharField(max_length=10, help_text='Eg- A, B, C etc')
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        unique_together = (('class_name', 'section'),)

    def __str__(self):
        return "%s Section-%s" % (self.class_name, self.section)

    def get_next_class(self):
        # Define the order of classes explicitly
        class_order = ["IST", "2ND", "3RD", "4TH", "5TH", "6TH", "7TH", "8TH", "Graduated",]

        try:
            current_index = class_order.index(self.class_name.upper())
            next_class_name = class_order[current_index + 1]  # Get the next class in the order
        except (ValueError, IndexError):
            return None  # Return None if current class is not in the list or if it's the last class

        try:
            return StudentClass.objects.get(class_name=next_class_name, section=self.section)
        except StudentClass.DoesNotExist:
            return None
