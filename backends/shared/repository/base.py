from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Type
from django.db import models


T = TypeVar('T', bound=models.Model)


class BaseRepository(Generic[T], ABC):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Must return a single entity by ID or None"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Must return all entities"""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Must add and return the entity"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Must update and return the entity"""
        pass
    
    @abstractmethod
    def delete(self, entity: T) -> None:
        """Must delete the entity"""
        pass
    
    @abstractmethod
    def filter(self, **kwargs) -> List[T]:
        """Must return filtered entities"""
        pass


class DjangoRepository(BaseRepository[T]):
    """Generic Django ORM repository for all models."""
    def get_by_id(self, id: int) -> Optional[T]:
        try:
            return self.model_class.objects.get(pk=id)
        except self.model_class.DoesNotExist:
            return None
    
    def get_all(self) -> List[T]:
        return list(self.model_class.objects.all())
    
    def create(self, data: dict) -> T:
        """Creates and saves a new instance from raw data."""
        return self.model_class.objects.create(**data)
    
    def update(self, id: int, data: dict) -> Optional[T]:
        """
        Updates an entity by ID and returns the updated object.
        Returns None if the ID doesn't exist.
        """
        updated_count = self.model_class.objects.filter(pk=id).update(**data)
        if updated_count == 0:
            return None
        return self.get_by_id(id)  # Reload the updated object
    
    def update_entity(self, entity: T, data: dict) -> T:
        """
        Updates an already-loaded entity and saves it.
        Useful for complex validations or signals.
        """
        for attr, value in data.items():
            setattr(entity, attr, value)
        entity.save()
        return entity

    def delete(self, id: int) -> bool:
        """
        Deletes an entity by ID. Returns True if deleted, False if not found.
        Uses efficient queryset deletion (no need to fetch object first).
        """
        deleted_count, _ = self.model_class.objects.filter(pk=id).delete()
        return deleted_count > 0

    def delete_entity(self, entity: T) -> None:
        """Deletes an already-loaded entity (use for custom deletion logic)."""
        entity.delete()
    
    def filter(self, **kwargs) -> List[T]:
        return list(self.model_class.objects.filter(**kwargs))